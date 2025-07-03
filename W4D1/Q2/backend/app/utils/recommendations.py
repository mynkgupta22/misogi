from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict

class RecommendationEngine:
    def __init__(self, products: List[Dict]):
        self.products = products
        self.product_features = self._prepare_product_features()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self._create_tfidf_matrix()
        self.similarity_matrix = self._create_similarity_matrix()

    def _prepare_product_features(self) -> List[str]:
        """Combine relevant product features into a single string for each product"""
        features = []
        for product in self.products:
            feature_text = f"{product['name']} {product['category']} {product['subcategory']} "
            feature_text += f"{product['description']} "
            feature_text += " ".join(product['tags'])
            feature_text += " ".join(product['features'])
            features.append(feature_text.lower())
        return features

    def _create_tfidf_matrix(self):
        """Create TF-IDF matrix from product features"""
        return self.tfidf.fit_transform(self.product_features)

    def _create_similarity_matrix(self):
        """Create similarity matrix using cosine similarity"""
        return cosine_similarity(self.tfidf_matrix)

    def get_similar_products(self, product_id: str, n: int = 5) -> List[Dict]:
        """Get n most similar products to a given product"""
        try:
            # Find product index
            product_idx = next(
                i for i, p in enumerate(self.products) 
                if p['id'] == product_id
            )
            
            # Get similarity scores
            similarity_scores = self.similarity_matrix[product_idx]
            
            # Get indices of most similar products (excluding self)
            similar_indices = similarity_scores.argsort()[::-1][1:n+1]
            
            # Return similar products
            return [self.products[i] for i in similar_indices]
        except StopIteration:
            return []

    def get_personalized_recommendations(
        self, 
        user_interactions: Dict[str, List[str]], 
        n: int = 5
    ) -> List[Dict]:
        """Get personalized recommendations based on user interactions"""
        if not any(user_interactions.values()):
            # If no interactions, return highest rated products
            return sorted(
                self.products, 
                key=lambda x: (x['rating'] * x['reviews_count']), 
                reverse=True
            )[:n]

        # Weight different types of interactions
        weights = {
            'viewed': 1,
            'liked': 2,
            'purchased': 3
        }

        # Calculate weighted average similarity
        weighted_scores = np.zeros(len(self.products))
        interaction_count = 0

        for interaction_type, product_ids in user_interactions.items():
            for product_id in product_ids:
                try:
                    product_idx = next(
                        i for i, p in enumerate(self.products) 
                        if p['id'] == product_id
                    )
                    weighted_scores += (
                        self.similarity_matrix[product_idx] * 
                        weights[interaction_type]
                    )
                    interaction_count += weights[interaction_type]
                except StopIteration:
                    continue

        if interaction_count > 0:
            weighted_scores /= interaction_count

        # Get indices of top recommendations (excluding already interacted products)
        interacted_products = set(
            pid for pids in user_interactions.values() for pid in pids
        )
        
        # Create mask for non-interacted products
        available_mask = np.ones(len(self.products), dtype=bool)
        for i, product in enumerate(self.products):
            if product['id'] in interacted_products:
                available_mask[i] = False

        # Apply mask and get top n recommendations
        masked_scores = weighted_scores * available_mask
        recommended_indices = masked_scores.argsort()[::-1][:n]

        return [self.products[i] for i in recommended_indices] 
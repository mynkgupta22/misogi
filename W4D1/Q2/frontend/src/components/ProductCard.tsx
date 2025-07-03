import React from 'react';
import Image from 'next/image';
import { HeartIcon, ShoppingCartIcon } from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import { products } from '@/lib/api';
import { useAuth } from '@/lib/auth-context';

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  image_url: string;
  rating: number;
  reviews_count: number;
  category: string;
  subcategory: string;
}

interface ProductCardProps {
  product: Product;
  onInteraction?: () => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onInteraction }) => {
  const { user } = useAuth();
  const isLiked = user?.interactions.liked.includes(product.id);

  const handleInteraction = async (type: 'viewed' | 'liked' | 'purchased') => {
    if (!user) return;
    try {
      await products.trackInteraction(product.id, type);
      onInteraction?.();
    } catch (error) {
      console.error(`Failed to track ${type} interaction:`, error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="relative h-48">
        <Image
          src={product.image_url}
          alt={product.name}
          fill
          className="object-cover"
        />
      </div>
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {product.name}
            </h3>
            <p className="text-sm text-gray-500">
              {product.category} &gt; {product.subcategory}
            </p>
          </div>
          <button
            onClick={() => handleInteraction('liked')}
            className="text-gray-400 hover:text-red-500 transition-colors"
          >
            {isLiked ? (
              <HeartSolidIcon className="h-6 w-6 text-red-500" />
            ) : (
              <HeartIcon className="h-6 w-6" />
            )}
          </button>
        </div>
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
          {product.description}
        </p>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xl font-bold text-gray-900">${product.price}</p>
            <div className="flex items-center mt-1">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <svg
                    key={i}
                    className={`h-4 w-4 ${
                      i < Math.floor(product.rating)
                        ? 'text-yellow-400'
                        : 'text-gray-300'
                    }`}
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
                <span className="ml-1 text-sm text-gray-500">
                  ({product.reviews_count})
                </span>
              </div>
            </div>
          </div>
          <button
            onClick={() => handleInteraction('purchased')}
            className="flex items-center justify-center px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
          >
            <ShoppingCartIcon className="h-5 w-5 mr-1" />
            Buy Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard; 
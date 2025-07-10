import os
import requests
from typing import Dict, Optional
import markdown

class MediumService:
    def __init__(self):
        self.api_key = os.getenv("MEDIUM_API_KEY", "test-key")
        self.user_id = os.getenv("MEDIUM_USER_ID", "test-user-id")
        self.base_url = "https://api.medium.com/v1"
        self.is_test_mode = self.api_key == "test-key" or self.user_id == "test-user-id"
            
        if not self.is_test_mode:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

    def publish_post(self, title: str, content: str, tags: list[str] = None) -> Optional[str]:
        """
        Publish a post to Medium
        
        Args:
            title (str): Post title
            content (str): Post content in markdown format
            tags (list[str], optional): List of tags for the post
            
        Returns:
            Optional[str]: URL of the published post if successful, None otherwise
        """
        if self.is_test_mode:
            return f"https://medium.com/test-user/test-article-{title.lower().replace(' ', '-')}"
            
        try:
            # Convert markdown to HTML
            html_content = markdown.markdown(content)
            
            # Prepare the post data
            post_data = {
                "title": title,
                "contentFormat": "html",
                "content": html_content,
                "publishStatus": "public"
            }
            
            if tags:
                post_data["tags"] = tags
                
            # Create the post
            response = requests.post(
                f"{self.base_url}/users/{self.user_id}/posts",
                headers=self.headers,
                json=post_data
            )
            
            if response.status_code == 201:
                post_data = response.json()["data"]
                return post_data["url"]
            else:
                print(f"Error publishing to Medium: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Error publishing to Medium: {str(e)}")
            return None

    def get_user_publications(self) -> list[Dict]:
        """
        Get a list of publications the user can post to
        
        Returns:
            list[Dict]: List of publication data
        """
        if self.is_test_mode:
            return [{
                "id": "test-pub-id",
                "name": "Test Publication",
                "description": "A test publication for development",
                "url": "https://medium.com/test-publication"
            }]
            
        try:
            response = requests.get(
                f"{self.base_url}/users/{self.user_id}/publications",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()["data"]
            else:
                print(f"Error getting publications: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error getting publications: {str(e)}")
            return [] 
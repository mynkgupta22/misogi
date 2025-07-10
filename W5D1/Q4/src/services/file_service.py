import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import json
from slugify import slugify

class FileService:
    def __init__(self, base_dir: str = "content"):
        self.base_dir = Path(base_dir)
        self.ideas_dir = self.base_dir / "ideas"
        self.generated_dir = self.base_dir / "generated"
        self.published_dir = self.base_dir / "published"
        self.templates_dir = self.base_dir / "templates"
        
        # Ensure directories exist
        for dir_path in [self.ideas_dir, self.generated_dir, self.published_dir, self.templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def save_idea(self, title: str, description: str, keywords: List[str], target_audience: str) -> str:
        """
        Save a new content idea to the ideas directory
        
        Returns:
            str: Path to the saved idea file
        """
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(title)
        filename = f"{date_prefix}-{slug}.json"
        
        idea_data = {
            "title": title,
            "description": description,
            "keywords": keywords,
            "target_audience": target_audience,
            "created_at": datetime.now().isoformat(),
            "status": "idea"
        }
        
        file_path = self.ideas_dir / filename
        with open(file_path, 'w') as f:
            json.dump(idea_data, f, indent=2)
            
        return str(file_path)

    def save_generated_content(self, idea_file: str, content: str) -> str:
        """
        Save generated content to the generated directory
        
        Returns:
            str: Path to the saved content file
        """
        idea_path = Path(idea_file)
        with open(idea_path, 'r') as f:
            idea_data = json.load(f)
            
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        slug = slugify(idea_data["title"])
        filename = f"{date_prefix}-{slug}.md"
        
        file_path = self.generated_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
            
        # Update idea status
        idea_data["status"] = "generated"
        idea_data["generated_file"] = str(file_path)
        idea_data["generated_at"] = datetime.now().isoformat()
        
        with open(idea_path, 'w') as f:
            json.dump(idea_data, f, indent=2)
            
        return str(file_path)

    def move_to_published(self, generated_file: str, medium_url: str = None) -> str:
        """
        Move a generated file to the published directory and update its metadata
        
        Returns:
            str: Path to the published file
        """
        source_path = Path(generated_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Generated file not found: {generated_file}")
            
        # Move the file to published directory
        target_path = self.published_dir / source_path.name
        
        # Read the content
        with open(source_path, 'r') as f:
            content = f.read()
            
        # Add Medium URL as metadata if provided
        if medium_url:
            metadata = {
                "published_at": datetime.now().isoformat(),
                "medium_url": medium_url
            }
            content = f"""---
{json.dumps(metadata, indent=2)}
---

{content}"""
            
        # Write to new location
        with open(target_path, 'w') as f:
            f.write(content)
            
        # Remove the original file
        source_path.unlink()
        
        return str(target_path)

    def get_content_status(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the status of all content in the workspace
        
        Returns:
            Dict with lists of content in each stage (ideas, generated, published)
        """
        status = {
            "ideas": [],
            "generated": [],
            "published": []
        }
        
        # Get ideas
        for file in self.ideas_dir.glob("*.json"):
            with open(file, 'r') as f:
                idea_data = json.load(f)
                status["ideas"].append({
                    "file": str(file),
                    "data": idea_data
                })
                
        # Get generated content
        for file in self.generated_dir.glob("*.md"):
            status["generated"].append({
                "file": str(file),
                "title": file.stem
            })
            
        # Get published content
        for file in self.published_dir.glob("*.md"):
            with open(file, 'r') as f:
                content = f.read()
                # Try to extract metadata
                metadata = {}
                if content.startswith("---"):
                    try:
                        metadata_end = content.find("---", 3)
                        metadata_str = content[3:metadata_end]
                        metadata = json.loads(metadata_str)
                    except:
                        pass
                        
            status["published"].append({
                "file": str(file),
                "title": file.stem,
                "metadata": metadata
            })
            
        return status 
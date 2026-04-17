import imagehash
from PIL import Image
import requests
from io import BytesIO
class ImageComparator:
    def __init__(self, hash_size=8):
        """
        hash_size 8 creates a 64-bit hash (8x8). 
        Increase to 16 for higher precision with crops.
        """
        self.hash_size = hash_size




    def get_phash(self, image_source):
        try:
            
            if image_source.startswith(('http://', 'https://')):
                response = requests.get(image_source, timeout=10)
                response.raise_for_status() 
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(image_source)

            return imagehash.phash(img, hash_size=self.hash_size)
            
        except Exception as e:
            print(e)
            return "error"
    def compare_hashes(self, hash1, hash2):
        """
        Compares two hashes and returns a similarity score.
        A distance of 0 means the images are structurally identical.
        """
        # Calculate Hamming Distance (number of bits that differ)
        distance = hash1 - hash2
        
        # Calculate similarity percentage
        # Max distance is hash_size squared (e.g., 8*8 = 64)
        max_distance = self.hash_size ** 2
        similarity = ((max_distance - distance) / max_distance) * 100
        
        return {
            "hamming_distance": distance,
            "similarity_percentage": round(similarity, 2)
        }
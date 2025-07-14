"""
Video Test Simulator for Pharmacy Inventory
Test your video before setting up the full system!
"""

import cv2
import numpy as np
from datetime import datetime
import json
import os
from typing import List, Dict
import base64

class VideoInventorySimulator:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.results = {
            "uploadId": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "products": [],
            "frameAnalysis": [],
            "summary": {}
        }
        
    def extract_frames(self, interval_seconds: float = 0.5):
        """Extract frames from video at specified interval"""
        print("📹 Extracting frames from video...")
        
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_seconds)
        
        frames = []
        frame_count = 0
        extracted_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                frames.append({
                    "frame": frame,
                    "frameNumber": frame_count,
                    "timestamp": frame_count / fps
                })
                extracted_count += 1
                
            frame_count += 1
            
        cap.release()
        print(f"✅ Extracted {extracted_count} frames from {frame_count} total frames")
        return frames
    
    def simulate_product_detection(self, frame_data: Dict) -> List[Dict]:
        """Simulate AI product detection on a frame"""
        frame = frame_data["frame"]
        
        # Simulate detection with random products (in real system, this would be AI)
        detections = []
        
        # Simulate 1-3 product detections per frame
        num_products = np.random.randint(1, 4)
        
        for i in range(num_products):
            # Simulate different scenarios
            scenario = np.random.choice([
                "normal", "normal", "normal",  # 60% normal
                "low_confidence",              # 10% low confidence
                "damaged",                     # 10% damaged
                "expired",                     # 10% expired  
                "unreadable"                   # 10% unreadable
            ])
            
            product = {
                "frameNumber": frame_data["frameNumber"],
                "timestamp": frame_data["timestamp"],
                "productId": f"MED-{np.random.randint(100, 999)}",
                "confidence": 0.95 if scenario == "normal" else np.random.uniform(0.5, 0.7),
                "quantity": np.random.randint(1, 20),
                "scenario": scenario
            }
            
            # Add scenario-specific data
            if scenario == "normal":
                product["expiryDate"] = "2025-12-31"
                product["status"] = "OK"
            elif scenario == "expired":
                product["expiryDate"] = "2023-06-15"
                product["status"] = "EXPIRED"
                product["alert"] = "Product expired!"
            elif scenario == "damaged":
                product["condition"] = "damaged"
                product["status"] = "REVIEW_REQUIRED"
                product["alert"] = "Damaged package detected"
            elif scenario == "unreadable":
                product["expiryDate"] = None
                product["status"] = "MANUAL_REVIEW"
                product["alert"] = "Cannot read expiry date"
                
            detections.append(product)
            
        return detections
    
    def process_video(self):
        """Main processing function"""
        print("\n🚀 Starting video analysis simulation...")
        
        # Extract frames
        frames = self.extract_frames()
        
        # Process each frame
        all_detections = []
        issues_found = {
            "expired": 0,
            "damaged": 0,
            "unreadable": 0,
            "low_confidence": 0
        }
        
        print("\n🔍 Analyzing frames...")
        for idx, frame_data in enumerate(frames):
            if idx % 10 == 0:
                print(f"Processing frame {idx}/{len(frames)}...")
                
            detections = self.simulate_product_detection(frame_data)
            all_detections.extend(detections)
            
            # Count issues
            for detection in detections:
                if detection.get("scenario") in issues_found:
                    issues_found[detection["scenario"]] += 1
        
        # Generate summary
        self.results["products"] = all_detections
        self.results["summary"] = {
            "totalFrames": len(frames),
            "totalProducts": len(all_detections),
            "uniqueProducts": len(set(d["productId"] for d in all_detections)),
            "highConfidence": len([d for d in all_detections if d["confidence"] > 0.9]),
            "lowConfidence": len([d for d in all_detections if d["confidence"] < 0.7]),
            "expired": issues_found["expired"],
            "damaged": issues_found["damaged"],
            "unreadable": issues_found["unreadable"],
            "requiresReview": sum([issues_found["damaged"], issues_found["unreadable"], issues_found["expired"]])
        }
        
        print("\n✅ Analysis complete!")
        
    def generate_report(self):
        """Generate a test report"""
        report = f"""
📊 VIDEO TEST REPORT
==================

Upload ID: {self.results['uploadId']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📹 Video Analysis Summary
------------------------
• Total Frames Analyzed: {self.results['summary']['totalFrames']}
• Total Products Detected: {self.results['summary']['totalProducts']}
• Unique Products: {self.results['summary']['uniqueProducts']}

🎯 Detection Confidence
----------------------
• High Confidence (>90%): {self.results['summary']['highConfidence']}
• Low Confidence (<70%): {self.results['summary']['lowConfidence']}
• Success Rate: {self.results['summary']['highConfidence'] / self.results['summary']['totalProducts'] * 100:.1f}%

⚠️ Issues Found
---------------
• Expired Products: {self.results['summary']['expired']}
• Damaged Products: {self.results['summary']['damaged']}
• Unreadable Dates: {self.results['summary']['unreadable']}
• Total Requiring Review: {self.results['summary']['requiresReview']}

📋 Sample Detections
-------------------"""
        
        # Add sample detections
        for i, product in enumerate(self.results['products'][:5]):
            report += f"\n{i+1}. Product {product['productId']} at {product['timestamp']:.1f}s"
            report += f"\n   Confidence: {product['confidence']:.0%}"
            if product.get('alert'):
                report += f"\n   ⚠️ {product['alert']}"
        
        if len(self.results['products']) > 5:
            report += f"\n... and {len(self.results['products']) - 5} more products"
        
        # Add recommendations
        report += "\n\n💡 Recommendations\n-----------------\n"
        
        if self.results['summary']['lowConfidence'] > self.results['summary']['totalProducts'] * 0.2:
            report += "• Video quality issue detected - try better lighting or slower movement\n"
            
        if self.results['summary']['requiresReview'] > 10:
            report += "• High number of manual reviews needed - consider rescanning problem areas\n"
            
        if self.results['summary']['expired'] > 0:
            report += "• Expired products found - immediate action required\n"
            
        report += "\n✅ Test simulation complete! Ready for real implementation."
        
        return report
    
    def save_results(self):
        """Save results to JSON file"""
        output_file = f"test_results_{self.results['uploadId']}.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
        
        # Save report
        report_file = f"test_report_{self.results['uploadId']}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        print(f"📄 Report saved to: {report_file}")

def main():
    """Main function to run the simulator"""
    print("🏥 Pharmacy Inventory Video Test Simulator")
    print("==========================================\n")
    
    # Get video file
    video_path = input("Enter path to your test video (or 'demo' for demo mode): ").strip()
    
    if video_path.lower() == 'demo':
        print("\n🎬 Running in demo mode with simulated video...")
        # Create a simple demo video
        create_demo_video()
        video_path = "demo_inventory_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file '{video_path}' not found!")
        return
    
    # Run simulation
    simulator = VideoInventorySimulator(video_path)
    simulator.process_video()
    
    # Show report
    print(simulator.generate_report())
    
    # Save results
    simulator.save_results()
    
    print("\n🎉 Simulation complete! Check the generated files for detailed results.")

def create_demo_video():
    """Create a simple demo video for testing"""
    print("Creating demo video...")
    
    # Create a simple video with colored rectangles representing products
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('demo_inventory_video.mp4', fourcc, 2.0, (640, 480))
    
    for i in range(20):  # 10 seconds at 2 fps
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        # Add some "products" (colored rectangles)
        cv2.rectangle(frame, (50, 50), (200, 200), (0, 255, 0), -1)
        cv2.putText(frame, f"Product {i}", (60, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        cv2.rectangle(frame, (250, 50), (400, 200), (255, 0, 0), -1)
        cv2.putText(frame, f"MED-{100+i}", (260, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print("✅ Demo video created: demo_inventory_video.mp4")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}") 
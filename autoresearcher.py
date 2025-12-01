"""
🤖 AutoResearcher: Your Personal AI Research Assistant
By: [Your Name]

This program uses 4 AI robots to do research automatically!
"""

import os
import asyncio
import time
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Try to import Google Genai
try:
    from google import genai
    print("✅ Google Genai imported successfully!")
except ImportError:
    print("❌ Error: google-genai not installed!")
    print("📝 Run: pip install google-genai")
    exit()

# Load environment variables (your API key)
load_dotenv()

print("\n" + "="*70)
print("🎉 WELCOME TO AUTORESEARCHER!")
print("="*70)
print("\n🤖 Your Personal AI Research Assistant")
print("💡 4 AI robots working together to create research papers!\n")

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Configuration settings"""
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-2.0-flash-exp"
    
    @classmethod
    def validate(cls):
        """Check if API key is set"""
        if not cls.API_KEY:
            print("❌ ERROR: API Key not found!")
            print("📝 Please add your key to the .env file")
            print("🔑 Get key from: https://aistudio.google.com/app/apikey")
            exit()
        print("✅ API Key loaded successfully!")

# Validate configuration
Config.validate()

# =============================================================================
# ROBOT MEMORY SYSTEM
# =============================================================================

class RobotMemory:
    """Helps robots remember things"""
    
    def __init__(self):
        self.memories: List[Dict] = []
        print("💾 Robot Memory System initialized")
    
    def remember(self, robot_name: str, what_happened: str):
        """Store a memory"""
        memory = {
            "robot": robot_name,
            "memory": what_happened,
            "time": datetime.now().strftime("%I:%M:%S %p")
        }
        self.memories.append(memory)
        print(f"   📝 {robot_name}: {what_happened[:50]}...")
    
    def recall_all(self):
        """Show all memories"""
        print("\n" + "="*70)
        print("💾 ROBOT MEMORY BANK")
        print("="*70)
        for i, memory in enumerate(self.memories, 1):
            print(f"\n{i}. [{memory['robot']}] at {memory['time']}")
            print(f"   {memory['memory']}")
        print()

# =============================================================================
# ROBOT TOOLS
# =============================================================================

class SearchTool:
    """Tool to search for research papers"""
    
    def search(self, topic: str) -> List[Dict]:
        """Search for papers about a topic"""
        print(f"   🔍 Searching for papers on: {topic}")
        
        # Mock papers (in real version, would use real search API)
        papers = [
            {
                "title": f"Recent Advances in {topic}: A Comprehensive Study",
                "summary": f"This groundbreaking paper explores {topic} using innovative methodologies and demonstrates significant improvements over existing approaches.",
                "source": "Nature AI",
                "year": "2024"
            },
            {
                "title": f"Understanding {topic}: Theory and Practice",
                "summary": f"An in-depth analysis of {topic} with practical applications, showing real-world impact and future research directions.",
                "source": "Science Direct",
                "year": "2024"
            },
            {
                "title": f"{topic}: State of the Art Review",
                "summary": f"A comprehensive review of current research in {topic}, identifying key trends, challenges, and opportunities.",
                "source": "IEEE Xplore",
                "year": "2024"
            }
        ]
        
        print(f"   ✅ Found {len(papers)} relevant papers!")
        return papers

class ExperimentTool:
    """Tool to run experiments"""
    
    def run_experiment(self, hypothesis: str) -> Dict:
        """Run a simple experiment"""
        print(f"   🧪 Running experiment: {hypothesis}")
        
        import random
        
        # Simulate experiment results
        result = {
            "hypothesis": hypothesis,
            "sample_size": random.randint(50, 200),
            "success_rate": round(random.uniform(0.65, 0.95), 2),
            "confidence": "95%",
            "status": "✅ Success"
        }
        
        print(f"   ✅ Experiment completed successfully!")
        return result

# =============================================================================
# THE 4 AI ROBOTS
# =============================================================================

class LibraryRobot:
    """Robot #1: Searches and analyzes research papers"""
    
    def __init__(self, model, memory: RobotMemory):
        self.name = "📚 Library Robot"
        self.model = model
        self.memory = memory
        self.search_tool = SearchTool()
        print(f"✅ {self.name} created!")
    
    async def research(self, topic: str) -> Dict:
        """Find and analyze papers"""
        print(f"\n{'='*70}")
        print(f"{self.name} is working on: {topic}")
        print('='*70)
        
        # Search for papers
        papers = self.search_tool.search(topic)
        
        # Create prompt for AI analysis
        papers_text = "\n\n".join([
            f"Paper {i+1}: {p['title']}\n"
            f"Source: {p['source']} ({p['year']})\n"
            f"Summary: {p['summary']}"
            for i, p in enumerate(papers)
        ])
        
        prompt = f"""You are an expert research analyst. Analyze these papers about "{topic}":

{papers_text}

Provide a clear summary (4-5 sentences) covering:
1. Main findings across these papers
2. Key trends and patterns
3. Important insights for new research

Write in simple, clear language."""

        # Get AI analysis
        response = await self.model.generate_content_async(prompt)
        
        # Remember this work
        self.memory.remember(self.name, f"Analyzed {len(papers)} papers on {topic}")
        
        print(f"\n✅ {self.name} completed analysis!")
        
        return {
            "robot": self.name,
            "papers_found": len(papers),
            "papers": papers,
            "analysis": response.text
        }


class ScienceRobot:
    """Robot #2: Designs and runs experiments"""
    
    def __init__(self, model, memory: RobotMemory):
        self.name = "🧪 Science Robot"
        self.model = model
        self.memory = memory
        self.experiment_tool = ExperimentTool()
        print(f"✅ {self.name} created!")
    
    async def conduct_experiments(self, topic: str, context: str) -> Dict:
        """Design and run experiments"""
        print(f"\n{'='*70}")
        print(f"{self.name} is working on: {topic}")
        print('='*70)
        
        # Ask AI to design experiments
        prompt = f"""You are a research scientist. Based on this topic: "{topic}"

Context: {context}

Design 2 simple experiments to test key hypotheses.

For each experiment, provide:
1. A clear hypothesis (one sentence)
2. Expected outcome (one sentence)

Format:
EXPERIMENT 1:
Hypothesis: [hypothesis]
Expected: [expected outcome]

EXPERIMENT 2:
Hypothesis: [hypothesis]
Expected: [expected outcome]

Keep it simple and practical."""

        # Get experiment designs
        response = await self.model.generate_content_async(prompt)
        
        # Run the experiments
        print("\n   Running experiments...")
        exp1 = self.experiment_tool.run_experiment("Testing hypothesis 1")
        exp2 = self.experiment_tool.run_experiment("Testing hypothesis 2")
        
        experiments = [exp1, exp2]
        
        # Remember this work
        self.memory.remember(self.name, f"Designed and ran {len(experiments)} experiments")
        
        print(f"\n✅ {self.name} completed experiments!")
        
        return {
            "robot": self.name,
            "experiment_count": len(experiments),
            "experiments": experiments,
            "design": response.text
        }


class TeacherRobot:
    """Robot #3: Reviews and provides feedback"""
    
    def __init__(self, model, memory: RobotMemory):
        self.name = "👨‍🏫 Teacher Robot"
        self.model = model
        self.memory = memory
        print(f"✅ {self.name} created!")
    
    async def review(self, library_work: Dict, science_work: Dict) -> Dict:
        """Review the research work"""
        print(f"\n{'='*70}")
        print(f"{self.name} is reviewing the work...")
        print('='*70)
        
        prompt = f"""You are a supportive peer reviewer.

LITERATURE REVIEW:
{library_work['analysis']}

EXPERIMENTAL WORK:
{science_work['design']}

Provide constructive feedback (4-5 sentences):
1. Strengths: What's good?
2. Suggestions: What could improve?
3. Overall assessment

Be encouraging and helpful!"""

        # Get review
        response = await self.model.generate_content_async(prompt)
        
        # Remember this work
        self.memory.remember(self.name, "Completed peer review of research")
        
        print(f"\n✅ {self.name} completed review!")
        
        return {
            "robot": self.name,
            "review": response.text
        }


class WriterRobot:
    """Robot #4: Writes the final research paper"""
    
    def __init__(self, model, memory: RobotMemory):
        self.name = "✍️ Writer Robot"
        self.model = model
        self.memory = memory
        print(f"✅ {self.name} created!")
    
    async def write_paper(self, topic: str, library: Dict, 
                         science: Dict, teacher: Dict) -> Dict:
        """Write the complete research paper"""
        print(f"\n{'='*70}")
        print(f"{self.name} is writing the paper...")
        print('='*70)
        
        prompt = f"""You are a research paper writer. Write a SHORT research paper on "{topic}".

Use this information:

LITERATURE FINDINGS:
{library['analysis']}

EXPERIMENTS CONDUCTED:
{science['design']}

PEER REVIEW:
{teacher['review']}

Write a complete paper with these sections:

1. INTRODUCTION (2-3 sentences: What is this about?)
2. LITERATURE REVIEW (2-3 sentences: What did others find?)
3. METHODOLOGY (2-3 sentences: What did we do?)
4. RESULTS (2-3 sentences: What did we find?)
5. CONCLUSION (2-3 sentences: What does it mean?)

Keep it clear, simple, and well-structured!"""

        # Generate paper
        response = await self.model.generate_content_async(prompt)
        
        # Save to file
        os.makedirs('output', exist_ok=True)
        filename = f"output/research_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{'='*70}\n")
            f.write(f"RESEARCH PAPER: {topic}\n")
            f.write(f"{'='*70}\n")
            f.write(f"Generated by AutoResearcher\n")
            f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
            f.write(f"{'='*70}\n\n")
            f.write(response.text)
            f.write(f"\n\n{'='*70}\n")
            f.write("End of Paper\n")
            f.write(f"{'='*70}\n")
        
        # Remember this work
        self.memory.remember(self.name, f"Wrote complete paper and saved to {filename}")
        
        print(f"\n✅ {self.name} completed paper!")
        print(f"   📄 Saved to: {filename}")
        
        return {
            "robot": self.name,
            "paper": response.text,
            "filename": filename
        }

# =============================================================================
# ORCHESTRATOR (Makes Robots Work Together)
# =============================================================================

class ResearchOrchestrator:
    """Coordinates all 4 robots to work together"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("🎯 INITIALIZING AUTORESEARCHER")
        print("="*70 + "\n")
        
        # Connect to AI
        self.client = genai.Client(api_key=Config.API_KEY)
        self.model = Config.MODEL_NAME
        print(f"🧠 AI Model connected: {Config.MODEL_NAME}")
        
        # Create memory system
        self.memory = RobotMemory()
        
        # Create all 4 robots
        print("\n🤖 Creating AI Robots:")
        self.library = LibraryRobot(self.model, self.memory)
        self.science = ScienceRobot(self.model, self.memory)
        self.teacher = TeacherRobot(self.model, self.memory)
        self.writer = WriterRobot(self.model, self.memory)
        
        print("\n✅ All systems ready!")
    
    async def run_research(self, topic: str):
        """Run the complete research pipeline"""
        print("\n" + "="*70)
        print(f"🔬 STARTING RESEARCH PROJECT")
        print("="*70)
        print(f"📋 Topic: {topic}")
        print(f"⏰ Start Time: {datetime.now().strftime('%I:%M:%S %p')}")
        print("="*70)
        
        start_time = time.time()
        
        # ===== PHASE 1: PARALLEL EXECUTION =====
        print("\n" + "▶"*35)
        print("⚡ PHASE 1: PARALLEL EXECUTION")
        print("📚 Library Robot + 🧪 Science Robot working TOGETHER!")
        print("▶"*35)
        
        phase1_start = time.time()
        
        # Both robots work at the SAME TIME!
        library_task = self.library.research(topic)
        science_task = self.science.conduct_experiments(
            topic, 
            "Initial research phase"
        )
        
        # Wait for both to finish
        library_result, science_result = await asyncio.gather(
            library_task,
            science_task
        )
        
        phase1_time = time.time() - phase1_start
        
        print(f"\n✅ PHASE 1 COMPLETE in {phase1_time:.1f} seconds")
        print(f"   📄 Papers analyzed: {library_result['papers_found']}")
        print(f"   🧪 Experiments run: {science_result['experiment_count']}")
        
        # ===== PHASE 2: SEQUENTIAL - REVIEW =====
        print("\n" + "▶"*35)
        print("⚡ PHASE 2: REVIEW")
        print("👨‍🏫 Teacher Robot checking the work...")
        print("▶"*35)
        
        phase2_start = time.time()
        
        teacher_result = await self.teacher.review(
            library_result,
            science_result
        )
        
        phase2_time = time.time() - phase2_start
        
        print(f"\n✅ PHASE 2 COMPLETE in {phase2_time:.1f} seconds")
        
        # ===== PHASE 3: SEQUENTIAL - WRITING =====
        print("\n" + "▶"*35)
        print("⚡ PHASE 3: WRITING")
        print("✍️ Writer Robot creating final paper...")
        print("▶"*35)
        
        phase3_start = time.time()
        
        writer_result = await self.writer.write_paper(
            topic,
            library_result,
            science_result,
            teacher_result
        )
        
        phase3_time = time.time() - phase3_start
        
        print(f"\n✅ PHASE 3 COMPLETE in {phase3_time:.1f} seconds")
        
        # ===== SHOW RESULTS =====
        total_time = time.time() - start_time
        
        print("\n" + "="*70)
        print("🎉 RESEARCH PROJECT COMPLETE!")
        print("="*70)
        print(f"\n⏱️  Total Time: {total_time:.1f} seconds")
        print(f"📊 Breakdown:")
        print(f"   Phase 1 (Parallel): {phase1_time:.1f}s")
        print(f"   Phase 2 (Review): {phase2_time:.1f}s")
        print(f"   Phase 3 (Writing): {phase3_time:.1f}s")
        print(f"\n🤖 Robots Used: 4")
        print(f"💾 Memories Stored: {len(self.memory.memories)}")
        print(f"📄 Paper Location: {writer_result['filename']}")
        print("="*70)
        
        # Show memory bank
        self.memory.recall_all()
        
        # Show results
        print("\n" + "="*70)
        print("📊 DETAILED RESULTS")
        print("="*70)
        
        print("\n📚 LITERATURE REVIEW:")
        print("-"*70)
        print(library_result['analysis'])
        
        print("\n\n🧪 EXPERIMENTS:")
        print("-"*70)
        print(science_result['design'])
        
        print("\n\n👨‍🏫 PEER REVIEW:")
        print("-"*70)
        print(teacher_result['review'])
        
        print("\n\n✍️ FINAL PAPER:")
        print("-"*70)
        print(writer_result['paper'])
        
        print("\n" + "="*70)
        print(f"📄 Full paper saved to: {writer_result['filename']}")
        print(f"📁 Check your 'output' folder!")
        print("="*70)
        
        return {
            "topic": topic,
            "total_time": total_time,
            "library": library_result,
            "science": science_result,
            "teacher": teacher_result,
            "writer": writer_result
        }

# =============================================================================
# MAIN PROGRAM
# =============================================================================

async def main():
    """Main function to run the program"""
    
    print("\n" + "🌟"*35)
    print("         WELCOME TO AUTORESEARCHER!")
    print("    Your Personal AI Research Assistant")
    print("🌟"*35 + "\n")
    
    # Get research topic from user
    print("What would you like to research today?")
    print("\nExamples:")
    print("  - Artificial Intelligence in Education")
    print("  - Climate Change Solutions")
    print("  - Quantum Computing Applications")
    print("  - Space Exploration Technologies")
    print()
    
    topic = input("Enter your research topic: ").strip()
    
    if not topic:
        topic = "Artificial Intelligence in Education"
        print(f"\n📋 Using default topic: {topic}")
    
    print(f"\n✅ Great choice! Starting research on: {topic}")
    
    # Create orchestrator
    orchestrator = ResearchOrchestrator()
    
    # Run the research!
    try:
        results = await orchestrator.run_research(topic)
        
        print("\n\n" + "🎉"*35)
        print("         SUCCESS!")
        print("🎉"*35)
        print(f"\n✅ Your research paper is complete!")
        print(f"📄 File: {results['writer']['filename']}")
        print(f"⏱️  Time taken: {results['total_time']:.1f} seconds")
        print("\n💡 Tip: Check the 'output' folder for your paper!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("💡 Make sure your API key is correct in the .env file")

# Run the program!
if __name__ == "__main__":
    print("\n🚀 Starting AutoResearcher...")
    asyncio.run(main())
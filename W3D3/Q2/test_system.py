#!/usr/bin/env python3
"""
Test script for the AI Coding Agent Recommendation System
"""

import json
import sys
from recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    """Test the recommendation engine functionality"""
    print("🧪 Testing Recommendation Engine...")
    
    try:
        # Initialize engine
        engine = RecommendationEngine()
        print(f"✅ Loaded {len(engine.agents)} agents successfully")
        
        # Test task analysis
        test_tasks = [
            "I need to build a REST API with Python Flask",
            "I want to debug a complex C++ algorithm with memory leaks",
            "Building a serverless app on AWS with Lambda and DynamoDB",
            "Creating a React frontend with TypeScript for a chat app"
        ]
        
        for i, task in enumerate(test_tasks, 1):
            print(f"\n📝 Test Task {i}: {task}")
            
            # Analyze task
            analysis = engine.analyze_task(task)
            print(f"   Complexity: {analysis['complexity']}")
            print(f"   Languages: {analysis['languages']}")
            print(f"   Domains: {analysis['domains']}")
            
            # Get recommendations
            recommendations = engine.get_recommendations(task)
            print(f"   Top recommendation: {recommendations[0]['agent']['name']} ({recommendations[0]['match_percentage']}% match)")
            print(f"   Justification: {recommendations[0]['justification']}")
        
        print("\n✅ All recommendation engine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Recommendation engine test failed: {e}")
        return False

def test_agent_database():
    """Test the agent database"""
    print("\n🧪 Testing Agent Database...")
    
    try:
        with open('agents_db.json', 'r') as f:
            data = json.load(f)
        
        agents = data.get('agents', [])
        print(f"✅ Loaded {len(agents)} agents from database")
        
        # Check required fields for each agent
        required_fields = ['id', 'name', 'description', 'capabilities', 'strengths', 'weaknesses', 'best_for', 'system_prompt', 'score_weights']
        
        for agent in agents:
            missing_fields = [field for field in required_fields if field not in agent]
            if missing_fields:
                print(f"❌ Agent '{agent.get('name', 'Unknown')}' missing fields: {missing_fields}")
                return False
        
        print("✅ All agents have required fields")
        return True
        
    except Exception as e:
        print(f"❌ Agent database test failed: {e}")
        return False

def test_flask_imports():
    """Test Flask imports"""
    print("\n🧪 Testing Flask Imports...")
    
    try:
        from flask import Flask, render_template, request, jsonify
        print("✅ Flask imports successful")
        return True
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Coding Agent Recommendation System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_flask_imports,
        test_agent_database,
        test_recommendation_engine
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n🚀 To start the application:")
        print("   python3 app.py")
        print("   Then open http://localhost:5000 in your browser")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
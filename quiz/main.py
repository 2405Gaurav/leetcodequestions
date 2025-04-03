from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
import os
from typing import List, Dict, Optional
import json
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

# API endpoints
LEETCODE_API_URL = "https://leetcode.com/api/problems/all/"
GFG_API_URL = "https://practice.geeksforgeeks.org/api/v1/problems/all/"
HACKERRANK_API_URL = "https://www.hackerrank.com/rest/contests/master/challenges"
CODING_NINJAS_API_URL = "https://www.codingninjas.com/api/v3/courses/2/problems"
CODE360_API_URL = "https://www.codingninjas.com/api/v3/courses/2/problems"

# Headers to mimic browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

# Company keywords mapping with expanded keywords
COMPANY_KEYWORDS = {
    "amazon": [
        "amazon", "aws", "prime", "echo", "alexa", "kindle",
        "s3", "ec2", "lambda", "dynamodb", "rds", "amazon web services",
        "amazon prime", "amazon echo", "amazon alexa", "amazon s3"
    ],
    "microsoft": [
        "microsoft", "azure", "windows", "office", "xbox", "bing", "linkedin",
        "microsoft azure", "microsoft office", "microsoft teams", "microsoft edge"
    ],
    "google": [
        "google", "gcp", "android", "chrome", "youtube", "maps", "search",
        "google cloud", "google maps", "google drive", "google docs"
    ],
    "meta": [
        "meta", "facebook", "instagram", "whatsapp", "oculus", "messenger",
        "meta platforms", "facebook messenger", "instagram api"
    ],
    "apple": [
        "apple", "ios", "macos", "iphone", "ipad", "macbook", "siri",
        "apple ios", "apple macos", "apple watch", "apple tv"
    ],
    "netflix": [
        "netflix", "streaming", "netflix api", "netflix original",
        "netflix recommendation", "netflix content"
    ],
    "uber": [
        "uber", "rideshare", "uber eats", "uber api", "uber driver",
        "uber passenger", "uber pool"
    ],
    "airbnb": [
        "airbnb", "booking", "airbnb api", "airbnb host",
        "airbnb guest", "airbnb listing"
    ]
}

def fetch_leetcode_questions() -> List[Dict]:
    """Fetch all questions from LeetCode API"""
    try:
        response = requests.get(LEETCODE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        questions = data.get("stat_status_pairs", [])
        print(f"✅ Fetched {len(questions)} questions from LeetCode")
        return questions
    except Exception as e:
        print(f"❌ Error fetching LeetCode questions: {str(e)}")
        return []

def fetch_gfg_questions() -> List[Dict]:
    """Fetch all questions from GFG API"""
    try:
        response = requests.get(GFG_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        questions = data.get("problems", [])
        print(f"✅ Fetched {len(questions)} questions from GeeksforGeeks")
        return questions
    except Exception as e:
        print(f"❌ Error fetching GFG questions: {str(e)}")
        return []

def fetch_hackerrank_questions() -> List[Dict]:
    """Fetch all questions from HackerRank API"""
    try:
        response = requests.get(HACKERRANK_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        questions = data.get("models", [])
        print(f"✅ Fetched {len(questions)} questions from HackerRank")
        return questions
    except Exception as e:
        print(f"❌ Error fetching HackerRank questions: {str(e)}")
        return []

def fetch_coding_ninjas_questions() -> List[Dict]:
    """Fetch all questions from Coding Ninjas API"""
    try:
        response = requests.get(CODING_NINJAS_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        questions = data.get("data", {}).get("problems", [])
        print(f"✅ Fetched {len(questions)} questions from Coding Ninjas")
        return questions
    except Exception as e:
        print(f"❌ Error fetching Coding Ninjas questions: {str(e)}")
        return []

def fetch_code360_questions() -> List[Dict]:
    """Fetch all questions from Code360 API"""
    try:
        response = requests.get(CODE360_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        questions = data.get("data", {}).get("problems", [])
        print(f"✅ Fetched {len(questions)} questions from Code360")
        return questions
    except Exception as e:
        print(f"❌ Error fetching Code360 questions: {str(e)}")
        return []

def get_company_questions(company: str, difficulty: Optional[str] = None) -> List[Dict]:
    """Get company-specific questions from all platforms"""
    if company.lower() not in COMPANY_KEYWORDS:
        return []
    
    keywords = COMPANY_KEYWORDS[company.lower()]
    all_questions = []
    
    # Fetch from all platforms
    platforms = [
        ("LeetCode", fetch_leetcode_questions),
        ("GeeksforGeeks", fetch_gfg_questions),
        ("HackerRank", fetch_hackerrank_questions),
        ("Coding Ninjas", fetch_coding_ninjas_questions),
        ("Code360", fetch_code360_questions)
    ]
    
    for platform_name, fetch_func in platforms:
        try:
            questions = fetch_func()
            for q in questions:
                # Skip paid questions
                if q.get("paid_only", False):
                    continue
                
                # Handle different platform data structures
                if platform_name == "LeetCode":
                    stat = q.get("stat", {})
                    title = stat.get("question__title", "").lower()
                    question_difficulty = {1: "Easy", 2: "Medium", 3: "Hard"}.get(q.get("difficulty", {}).get("level", 0), "Unknown")
                    url = f"https://leetcode.com/problems/{stat.get('question__title_slug', '')}/"
                    total_accepted = stat.get("total_acs", 0)
                    total_submitted = stat.get("total_submitted", 0)
                
                elif platform_name == "GeeksforGeeks":
                    title = q.get("title", "").lower()
                    question_difficulty = q.get("difficulty", "Unknown")
                    url = f"https://practice.geeksforgeeks.org/problems/{q.get('slug', '')}"
                    total_accepted = q.get("accepted", 0)
                    total_submitted = q.get("submitted", 0)
                
                elif platform_name == "HackerRank":
                    title = q.get("name", "").lower()
                    question_difficulty = q.get("difficulty_name", "Unknown")
                    url = f"https://www.hackerrank.com/challenges/{q.get('slug', '')}"
                    total_accepted = q.get("success_ratio", 0) * q.get("total_submissions", 0)
                    total_submitted = q.get("total_submissions", 0)
                
                else:  # Coding Ninjas and Code360
                    title = q.get("title", "").lower()
                    question_difficulty = q.get("difficulty", "Unknown")
                    url = q.get("url", "")
                    total_accepted = q.get("accepted", 0)
                    total_submitted = q.get("submitted", 0)
                
                # Check if question matches company keywords
                if any(keyword in title for keyword in keywords):
                    # Apply difficulty filter if specified
                    if difficulty and question_difficulty.lower() != difficulty.lower():
                        continue
                    
                    # Calculate acceptance rate
                    acceptance_rate = f"{(total_accepted / total_submitted * 100):.1f}%" if total_submitted > 0 else "N/A"
                    
                    question_data = {
                        "platform": platform_name,
                        "title": title.title(),
                        "difficulty": question_difficulty,
                        "url": url,
                        "total_accepted": total_accepted,
                        "total_submitted": total_submitted,
                        "acceptance_rate": acceptance_rate
                    }
                    all_questions.append(question_data)
                    
        except Exception as e:
            print(f"❌ Error processing {platform_name} questions: {str(e)}")
            continue
    
    return all_questions

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """API endpoint to get list of supported companies"""
    return jsonify({
        "status": "success",
        "companies": list(COMPANY_KEYWORDS.keys())
    })

@app.route('/api/questions/<company>', methods=['GET'])
def get_company_questions_endpoint(company):
    """API endpoint to get company-specific questions"""
    try:
        difficulty = request.args.get('difficulty')
        questions = get_company_questions(company, difficulty)
        
        # Calculate difficulty distribution
        difficulty_dist = {
            "easy": sum(1 for q in questions if q['difficulty'].lower() == 'easy'),
            "medium": sum(1 for q in questions if q['difficulty'].lower() == 'medium'),
            "hard": sum(1 for q in questions if q['difficulty'].lower() == 'hard')
        }
        
        # Calculate platform distribution
        platform_dist = {
            platform.lower().replace(" ", ""): sum(1 for q in questions if q['platform'] == platform)
            for platform in ["LeetCode", "GeeksforGeeks", "HackerRank", "Coding Ninjas", "Code360"]
        }
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "company": company,
            "total_questions": len(questions),
            "difficulty_distribution": difficulty_dist,
            "platform_distribution": platform_dist,
            "questions": questions
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/summary/<company>', methods=['GET'])
def get_company_summary(company):
    """API endpoint to get summary of company-specific questions"""
    try:
        questions = get_company_questions(company)
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "company": company,
            "summary": {
                "total_questions": len(questions),
                "difficulty_distribution": {
                    "easy": sum(1 for q in questions if q['difficulty'].lower() == 'easy'),
                    "medium": sum(1 for q in questions if q['difficulty'].lower() == 'medium'),
                    "hard": sum(1 for q in questions if q['difficulty'].lower() == 'hard')
                },
                "platform_distribution": {
                    platform.lower().replace(" ", ""): sum(1 for q in questions if q['platform'] == platform)
                    for platform in ["LeetCode", "GeeksforGeeks", "HackerRank", "Coding Ninjas", "Code360"]
                }
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
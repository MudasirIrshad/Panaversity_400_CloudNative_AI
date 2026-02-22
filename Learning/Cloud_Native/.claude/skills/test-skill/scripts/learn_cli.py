#!/usr/bin/env python3
"""
Interactive Learning Launcher

This script provides a simple interface to start and manage interactive learning sessions.
"""

import sys
import os
# Add the parent directory to the path to import the interactive_learning module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from interactive_learning import (
    start_learning,
    get_learning_step,
    submit_answer,
    get_progress,
    DifficultyLevel,
    LearningStyle
)

def main():
    print("🎓 Interactive Learning System")
    print("=" * 40)

    # Get user information
    user_id = input("Enter your username/nickname: ").strip()
    if not user_id:
        user_id = "learner"

    # Get topic to learn
    print("\nAvailable topics:")
    print("- Docker (recommended for beginners)")
    print("- Other topics can be added")

    topic = input("\nWhat would you like to learn today? ").strip()
    if not topic:
        topic = "Docker"

    # Get difficulty preference
    print("\nDifficulty levels:")
    print("1. Beginner (start with fundamentals)")
    print("2. Intermediate (assumes basic knowledge)")
    print("3. Advanced (deep dive into complex topics)")

    difficulty_choice = input("\nChoose difficulty (1-3, default 1): ").strip()
    difficulty_map = {
        "1": "beginner",
        "2": "intermediate",
        "3": "advanced",
        "": "beginner"
    }
    difficulty = difficulty_map.get(difficulty_choice, "beginner")

    # Get learning style
    print("\nLearning styles:")
    print("1. Visual (diagrams, visual aids)")
    print("2. Auditory (verbal explanations)")
    print("3. Kinesthetic (hands-on, practical)")

    style_choice = input("\nChoose learning style (1-3, default 1): ").strip()
    style_map = {
        "1": "visual",
        "2": "auditory",
        "3": "kinesthetic",
        "": "visual"
    }
    learning_style = style_map.get(style_choice, "visual")

    # Start the learning session
    print(f"\n🚀 Starting your learning session...")
    welcome_msg = start_learning(user_id, topic, difficulty, learning_style)
    print(welcome_msg)

    print("\n" + "="*50)
    print("YOUR LEARNING SESSION HAS STARTED")
    print("="*50)

    # Main learning loop
    session_active = True
    while session_active:
        step = get_learning_step(user_id)

        if step["type"] == "completion":
            print(step["message"])
            session_active = False
            break
        elif step["type"] == "concept":
            print(f"\n{step['message']}")

            if step["quiz"]:
                print(f"\n🤔 **QUIZ TIME!**")
                print(f"Question: {step['quiz']['text']}")

                for option in step["quiz"]["options"]:
                    print(f"  {option}")

                answer = input("\nYour answer (enter the letter/number): ").strip()

                result = submit_answer(user_id, step["quiz"]["id"], answer)

                print(f"\n📊 **FEEDBACK:**")
                print(result["feedback"])

                continue_learning = input("\nPress Enter to continue learning or 'q' to quit: ").strip().lower()
                if continue_learning == 'q':
                    print("\n📚 Session paused. Your progress has been saved.")
                    print(get_progress(user_id))
                    session_active = False
            else:
                print("\nNo quiz for this concept. Moving to next...")
                input("Press Enter to continue...")
        else:
            print(f"Error: {step['message']}")
            session_active = False

    print("\n🎓 Thank you for learning with us!")
    print("Feel free to come back anytime to continue your learning journey!")


if __name__ == "__main__":
    main()
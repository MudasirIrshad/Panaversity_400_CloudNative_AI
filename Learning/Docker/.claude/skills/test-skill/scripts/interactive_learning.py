"""
Interactive Learning and Quiz System

This module provides an adaptive learning system that guides users through
educational content with interactive quizzes, progress tracking, and
personalized feedback.
"""

import json
import random
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"


@dataclass
class Question:
    id: str
    text: str
    options: List[str]
    correct_answer: str
    explanation: str
    difficulty: DifficultyLevel
    category: str


@dataclass
class Concept:
    id: str
    title: str
    description: str
    examples: List[str]
    key_points: List[str]
    related_concepts: List[str]


@dataclass
class UserProgress:
    user_id: str
    current_topic: str
    current_concept_index: int
    completed_concepts: List[str]
    quiz_scores: Dict[str, float]
    total_questions_answered: int
    correct_answers: int
    learning_style: LearningStyle
    difficulty_preference: DifficultyLevel
    streak: int
    achievements: List[str]


class LearningManager:
    def __init__(self):
        self.concepts_db = {}
        self.questions_db = {}
        self.user_progress = {}
        self.current_session = None

    def register_topic(self, topic: str, concepts: List[Concept], questions: List[Question]):
        """Register a new topic with its concepts and questions."""
        self.concepts_db[topic] = concepts
        self.questions_db[topic] = questions

    def start_learning_session(self, user_id: str, topic: str,
                             difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
                             learning_style: LearningStyle = LearningStyle.VISUAL) -> str:
        """Start a new learning session for a user."""
        if topic not in self.concepts_db:
            return f"Topic '{topic}' not available. Please register concepts first."

        self.current_session = {
            'user_id': user_id,
            'topic': topic,
            'started_at': time.time()
        }

        # Initialize user progress if not exists
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                current_topic=topic,
                current_concept_index=0,
                completed_concepts=[],
                quiz_scores={},
                total_questions_answered=0,
                correct_answers=0,
                learning_style=learning_style,
                difficulty_preference=difficulty,
                streak=0,
                achievements=[]
            )
        else:
            # Update topic for existing user
            self.user_progress[user_id].current_topic = topic
            self.user_progress[user_id].current_concept_index = 0

        welcome_message = f"""
🎯 Welcome to your personalized learning session!
📚 Topic: {topic.title()}
🎯 Difficulty: {difficulty.value.title()}
🎨 Learning Style: {learning_style.value.title()}

Let's begin your learning journey. I'll guide you through concepts one at a time,
and then quiz you to reinforce your understanding.

Ready to start? Let's go! 🚀
        """
        return welcome_message

    def get_next_concept(self, user_id: str) -> Optional[tuple]:
        """Get the next concept for the user."""
        if user_id not in self.user_progress:
            return None

        progress = self.user_progress[user_id]
        topic = progress.current_topic

        if topic not in self.concepts_db:
            return None

        concepts = self.concepts_db[topic]

        if progress.current_concept_index >= len(concepts):
            # Learning session completed
            return None, "completed"

        concept = concepts[progress.current_concept_index]
        return concept, "concept"

    def present_concept(self, concept: Concept, learning_style: LearningStyle) -> str:
        """Present a concept based on learning style."""
        message = f"""
🔍 **CONCEPT: {concept.title.upper()}**

📝 **Description:**
{concept.description}

💡 **Key Points:**
"""
        for i, point in enumerate(concept.key_points, 1):
            message += f"{i}. {point}\n"

        if concept.examples:
            message += f"\n📋 **Examples:**\n"
            for example in concept.examples:
                message += f"• {example}\n"

        # Adapt presentation based on learning style
        if learning_style == LearningStyle.VISUAL:
            message += f"\n🎨 **Visual Aid:** Think of this concept as: [Visual representation would be helpful here]"
        elif learning_style == LearningStyle.AUDITORY:
            message += f"\n🗣️ **Memory Aid:** Try saying this concept aloud to remember it better."
        elif learning_style == LearningStyle.KINESTHETIC:
            message += f"\n动手 **Hands-on Tip:** Try applying this concept in a practical exercise."

        return message

    def get_quiz_for_concept(self, topic: str, concept_id: str, difficulty: DifficultyLevel) -> Optional[Question]:
        """Get a quiz question for a specific concept."""
        if topic not in self.questions_db:
            return None

        # Filter questions for this concept and difficulty
        concept_questions = [
            q for q in self.questions_db[topic]
            if concept_id in q.category and q.difficulty == difficulty
        ]

        # If no questions match difficulty, try lower difficulty
        if not concept_questions:
            if difficulty == DifficultyLevel.INTERMEDIATE:
                concept_questions = [
                    q for q in self.questions_db[topic]
                    if concept_id in q.category and q.difficulty == DifficultyLevel.BEGINNER
                ]
            elif difficulty == DifficultyLevel.ADVANCED:
                concept_questions = [
                    q for q in self.questions_db[topic]
                    if concept_id in q.category and q.difficulty in [DifficultyLevel.BEGINNER, DifficultyLevel.INTERMEDIATE]
                ]

        if concept_questions:
            return random.choice(concept_questions)
        return None

    def evaluate_answer(self, user_id: str, question: Question, user_answer: str) -> tuple:
        """Evaluate user's answer and update progress."""
        progress = self.user_progress[user_id]

        is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()

        # Update statistics
        progress.total_questions_answered += 1
        if is_correct:
            progress.correct_answers += 1
            progress.streak += 1
        else:
            progress.streak = 0  # Reset streak on wrong answer

        # Calculate current accuracy
        accuracy = progress.correct_answers / progress.total_questions_answered if progress.total_questions_answered > 0 else 0

        # Prepare feedback message
        if is_correct:
            feedback = f"""
✅ **CORRECT!** Great job!

💬 **Explanation:** {question.explanation}

🏆 **Streak:** {progress.streak} correct answers in a row!
📈 **Accuracy:** {accuracy:.1%} ({progress.correct_answers}/{progress.total_questions_answered})
            """
        else:
            feedback = f"""
❌ **INCORRECT** Don't worry, let's learn from this!

✅ **Correct Answer:** {question.correct_answer}
💬 **Explanation:** {question.explanation}

🔄 **Try again:** {question.text}
{chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(question.options)])}

📈 **Accuracy:** {accuracy:.1%} ({progress.correct_answers}/{progress.total_questions_answered})
            """

        return is_correct, feedback

    def advance_concept(self, user_id: str):
        """Advance to the next concept."""
        if user_id in self.user_progress:
            self.user_progress[user_id].current_concept_index += 1

    def get_progress_summary(self, user_id: str) -> str:
        """Get a summary of user's progress."""
        if user_id not in self.user_progress:
            return "No progress recorded yet."

        progress = self.user_progress[user_id]
        accuracy = progress.correct_answers / progress.total_questions_answered if progress.total_questions_answered > 0 else 0

        topic = progress.current_topic
        concepts = self.concepts_db.get(topic, [])
        completed_count = min(progress.current_concept_index, len(concepts))

        summary = f"""
📊 **PROGRESS SUMMARY**

📖 **Topic:** {topic}
🎯 **Concepts Completed:** {completed_count}/{len(concepts)}
✅ **Overall Accuracy:** {accuracy:.1%} ({progress.correct_answers}/{progress.total_questions_answered})
🔥 **Current Streak:** {progress.streak} correct answers
🎨 **Learning Style:** {progress.learning_style.value}
💪 **Achievements:** {len(progress.achievements)}

Keep up the great work! 🌟
        """
        return summary

    def get_learning_recommendations(self, user_id: str) -> str:
        """Provide personalized learning recommendations."""
        if user_id not in self.user_progress:
            return "Start learning to get personalized recommendations!"

        progress = self.user_progress[user_id]
        accuracy = progress.correct_answers / progress.total_questions_answered if progress.total_questions_answered > 0 else 0

        recommendations = "💡 **PERSONALIZED RECOMMENDATIONS**\n\n"

        if accuracy < 0.7:
            recommendations += "⚠️ Consider reviewing concepts at a slower pace and practicing more.\n"
        elif accuracy > 0.9:
            recommendations += "🚀 You're doing great! Consider advancing to more challenging material.\n"

        if progress.streak == 0:
            recommendations += "🔄 Take breaks between concepts to improve retention.\n"
        elif progress.streak > 5:
            recommendations += "🔥 You're on fire! Keep up the momentum!\n"

        recommendations += "\nKeep learning and growing! 🌱"
        return recommendations


# Global learning manager instance
learning_manager = LearningManager()


def initialize_docker_learning_content():
    """Initialize Docker learning content in the system."""

    # Docker concepts
    docker_concepts = [
        Concept(
            id="docker_fundamentals",
            title="Docker Fundamentals",
            description="Docker is a containerization platform that packages applications and their dependencies into standardized units called containers.",
            examples=[
                "Shipping containers analogy: Just like shipping containers standardize cargo transport, Docker containers standardize application deployment",
                "A Docker container can run a web server, database, or any application consistently across different environments"
            ],
            key_points=[
                "Containers are lightweight compared to virtual machines",
                "Share the host OS kernel",
                "Portable across different systems",
                "Isolate applications from each other"
            ],
            related_concepts=["vm_comparison", "container_vs_image"]
        ),
        Concept(
            id="vm_comparison",
            title="Containers vs Virtual Machines",
            description="Key differences between containerization and virtualization technologies.",
            examples=[
                "VMs: Each has a full OS, takes minutes to boot, GBs of space",
                "Containers: Share kernel, boot in seconds, MBs of space"
            ],
            key_points=[
                "VMs provide hardware virtualization",
                "Containers provide OS-level virtualization",
                "Containers are more resource-efficient",
                "VMs offer stronger isolation"
            ],
            related_concepts=["docker_fundamentals", "architecture"]
        ),
        Concept(
            id="architecture",
            title="Docker Architecture",
            description="The components that make up the Docker ecosystem.",
            examples=[
                "Docker Client talks to Docker Daemon",
                "Images stored in Docker Registry",
                "Containers run from Images"
            ],
            key_points=[
                "Client-server architecture",
                "Docker Daemon manages containers",
                "Images are templates for containers",
                "Registries store and distribute images"
            ],
            related_concepts=["docker_fundamentals", "commands"]
        ),
        Concept(
            id="commands",
            title="Essential Docker Commands",
            description="Basic commands needed to work with Docker.",
            examples=[
                "docker run: Start a container",
                "docker build: Build an image",
                "docker ps: List running containers"
            ],
            key_points=[
                "docker run [image]: Run a container",
                "docker build -t [name] .: Build an image",
                "docker ps -a: Show all containers",
                "docker stop [container]: Stop a container"
            ],
            related_concepts=["architecture", "dockerfile"]
        ),
        Concept(
            id="dockerfile",
            title="Dockerfile Basics",
            description="Text file containing instructions to build a Docker image.",
            examples=[
                "FROM: Set base image",
                "COPY: Copy files to container",
                "CMD: Set default command"
            ],
            key_points=[
                "Each instruction creates a layer",
                "Order matters for caching",
                "Use .dockerignore for sensitive files",
                "Minimize layers for efficiency"
            ],
            related_concepts=["commands", "compose"]
        ),
        Concept(
            id="compose",
            title="Docker Compose",
            description="Tool for defining and running multi-container Docker applications.",
            examples=[
                "Single file defines entire application stack",
                "Database, web server, and other services together",
                "docker-compose up starts everything"
            ],
            key_points=[
                "Uses YAML configuration file",
                "Manages multiple services",
                "Handles networking between containers",
                "Simplifies multi-container apps"
            ],
            related_concepts=["dockerfile", "security"]
        ),
        Concept(
            id="security",
            title="Docker Security",
            description="Best practices for securing Docker containers.",
            examples=[
                "Run containers as non-root users",
                "Scan images for vulnerabilities",
                "Use minimal base images"
            ],
            key_points=[
                "Avoid running as root",
                "Use trusted base images",
                "Limit container capabilities",
                "Regular updates and patches"
            ],
            related_concepts=["compose", "troubleshooting"]
        ),
        Concept(
            id="troubleshooting",
            title="Docker Troubleshooting",
            description="Common issues and solutions in Docker.",
            examples=[
                "Port already allocated errors",
                "Out of disk space issues",
                "Container keeps restarting"
            ],
            key_points=[
                "Check container logs first",
                "Verify resource limits",
                "Clean up unused resources",
                "Use proper error messages"
            ],
            related_concepts=["security"]
        )
    ]

    # Docker questions
    docker_questions = [
        Question(
            id="q1",
            text="What is the main advantage of Docker containers over Virtual Machines?",
            options=[
                "A) Stronger security isolation",
                "B) Faster boot times and lower resource usage",
                "C) Ability to run multiple operating systems",
                "D) Better performance for CPU-intensive tasks"
            ],
            correct_answer="B",
            explanation="Docker containers share the host OS kernel, allowing them to boot in seconds and use MBs of space, while VMs include full OSes and take minutes to boot with GBs of space.",
            difficulty=DifficultyLevel.BEGINNER,
            category="docker_fundamentals"
        ),
        Question(
            id="q2",
            text="What does the 'FROM' instruction in a Dockerfile do?",
            options=[
                "A) Copies files from host to container",
                "B) Specifies the base image to use",
                "C) Sets environment variables",
                "D) Defines the command to run"
            ],
            correct_answer="B",
            explanation="The FROM instruction sets the base image for subsequent instructions in the Dockerfile. A valid Dockerfile must start with a FROM instruction.",
            difficulty=DifficultyLevel.BEGINNER,
            category="dockerfile"
        ),
        Question(
            id="q3",
            text="Which command lists all Docker containers (including stopped ones)?",
            options=[
                "A) docker ps",
                "B) docker containers",
                "C) docker ps -a",
                "D) docker list all"
            ],
            correct_answer="C",
            explanation="docker ps shows only running containers. docker ps -a shows all containers including stopped ones. The -a flag means 'all'.",
            difficulty=DifficultyLevel.BEGINNER,
            category="commands"
        ),
        Question(
            id="q4",
            text="Why is it a security best practice to run containers as non-root users?",
            options=[
                "A) It improves performance",
                "B) It reduces image size",
                "C) It limits potential damage if the container is compromised",
                "D) It's required by Docker"
            ],
            correct_answer="C",
            explanation="Running as non-root limits the privileges available if an attacker compromises the container, reducing potential damage to the host system.",
            difficulty=DifficultyLevel.INTERMEDIATE,
            category="security"
        ),
        Question(
            id="q5",
            text="What is the purpose of Docker layers?",
            options=[
                "A) To separate applications",
                "B) To enable layer caching and efficient builds",
                "C) To improve security",
                "D) To manage networking"
            ],
            correct_answer="B",
            explanation="Docker layers enable caching, where unchanged layers can be reused, making builds faster and images more efficient by sharing common layers.",
            difficulty=DifficultyLevel.INTERMEDIATE,
            category="dockerfile"
        ),
        Question(
            id="q6",
            text="What does 'docker-compose up' do?",
            options=[
                "A) Builds Docker images",
                "B) Starts services defined in docker-compose.yml",
                "C) Stops running containers",
                "D) Lists all services"
            ],
            correct_answer="B",
            explanation="docker-compose up builds, (re)creates, starts, and attaches to containers for a service. It reads the docker-compose.yml file to start all defined services.",
            difficulty=DifficultyLevel.INTERMEDIATE,
            category="compose"
        ),
        Question(
            id="q7",
            text="In Docker, what's the difference between an image and a container?",
            options=[
                "A) Images are running instances, containers are templates",
                "B) Containers are read-only, images are writable",
                "C) Images are templates, containers are running instances",
                "D) There is no difference"
            ],
            correct_answer="C",
            explanation="An image is a read-only template with instructions for creating a Docker container. A container is a runnable instance of an image.",
            difficulty=DifficultyLevel.BEGINNER,
            category="docker_fundamentals"
        ),
        Question(
            id="q8",
            text="What does the -p flag do in 'docker run -p 8080:80 nginx'?",
            options=[
                "A) Sets the container priority",
                "B) Maps host port 8080 to container port 80",
                "C) Publishes all ports",
                "D) Sets the protocol to UDP"
            ],
            correct_answer="B",
            explanation="The -p flag maps network ports. The format is -p HOST_PORT:CONTAINER_PORT, so this maps port 8080 on the host to port 80 in the container.",
            difficulty=DifficultyLevel.INTERMEDIATE,
            category="commands"
        )
    ]

    learning_manager.register_topic("Docker", docker_concepts, docker_questions)


def start_learning(user_id: str, topic: str, difficulty: str = "beginner", learning_style: str = "visual"):
    """Start a learning session for a specific topic."""
    difficulty_enum = DifficultyLevel(difficulty.lower())
    style_enum = LearningStyle(learning_style.lower())

    # Initialize Docker content if not already done
    if not learning_manager.concepts_db:
        initialize_docker_learning_content()

    return learning_manager.start_learning_session(user_id, topic, difficulty_enum, style_enum)


def get_learning_step(user_id: str):
    """Get the next step in the learning process."""
    concept_data, status = learning_manager.get_next_concept(user_id)

    if status == "completed":
        return {
            "type": "completion",
            "message": "🎉 Congratulations! You've completed the learning session.\n\n" +
                      learning_manager.get_progress_summary(user_id) +
                      learning_manager.get_learning_recommendations(user_id)
        }
    elif concept_data:
        # Present concept
        progress = learning_manager.user_progress[user_id]
        message = learning_manager.present_concept(concept_data, progress.learning_style)

        # Add quiz for this concept
        quiz_question = learning_manager.get_quiz_for_concept(
            progress.current_topic,
            concept_data.id,
            progress.difficulty_preference
        )

        return {
            "type": "concept",
            "concept_id": concept_data.id,
            "message": message,
            "quiz": {
                "id": quiz_question.id if quiz_question else None,
                "text": quiz_question.text if quiz_question else None,
                "options": quiz_question.options if quiz_question else None,
                "explanation": quiz_question.explanation if quiz_question else None
            } if quiz_question else None
        }
    else:
        return {
            "type": "error",
            "message": "No learning content available. Please start a session first."
        }


def submit_answer(user_id: str, question_id: str, answer: str):
    """Submit an answer to a quiz question."""
    if user_id not in learning_manager.user_progress:
        return {"error": "No active learning session"}

    topic = learning_manager.user_progress[user_id].current_topic
    if topic not in learning_manager.questions_db:
        return {"error": "No questions available for this topic"}

    # Find the question
    question = None
    for q in learning_manager.questions_db[topic]:
        if q.id == question_id:
            question = q
            break

    if not question:
        return {"error": "Question not found"}

    is_correct, feedback = learning_manager.evaluate_answer(user_id, question, answer)

    # Advance to next concept if answer was correct (or after a few attempts)
    # For simplicity, we'll advance after each question
    learning_manager.advance_concept(user_id)

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "next_available": True
    }


def get_progress(user_id: str):
    """Get user's learning progress."""
    return learning_manager.get_progress_summary(user_id)


if __name__ == "__main__":
    # Initialize content
    initialize_docker_learning_content()

    print("Interactive Learning System Initialized!")
    print("Topics available:", list(learning_manager.concepts_db.keys()))
    print("\nAvailable commands:")
    print("- start_learning(user_id, topic, difficulty='beginner', learning_style='visual')")
    print("- get_learning_step(user_id)")
    print("- submit_answer(user_id, question_id, answer)")
    print("- get_progress(user_id)")
"""
Docker Helper Functions for Common Operations

This module provides utility functions for common Docker operations,
including container management, image operations, network management,
and troubleshooting utilities.
"""

import subprocess
import json
import os
import sys
from typing import Dict, List, Optional, Union
import docker
from pathlib import Path


class DockerHelper:
    """
    A comprehensive helper class for Docker operations.
    """

    def __init__(self):
        """Initialize Docker client."""
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Error connecting to Docker daemon: {e}")
            print("Make sure Docker is installed and running.")
            sys.exit(1)

    def run_container(self, image: str, name: Optional[str] = None,
                     ports: Optional[Dict[str, int]] = None,
                     volumes: Optional[Dict[str, dict]] = None,
                     detach: bool = True,
                     environment: Optional[Dict[str, str]] = None) -> str:
        """
        Run a Docker container with specified configurations.

        Args:
            image: Docker image to run
            name: Name for the container (optional)
            ports: Port mappings {container_port: host_port}
            volumes: Volume mappings {host_path: container_path}
            detach: Run in detached mode (default True)
            environment: Environment variables dict

        Returns:
            Container ID
        """
        try:
            container = self.client.containers.run(
                image=image,
                name=name,
                ports=ports,
                volumes=volumes,
                detach=detach,
                environment=environment
            )
            print(f"Successfully started container: {container.id[:12]}")
            return container.id
        except Exception as e:
            print(f"Error running container: {e}")
            return ""

    def build_image(self, path: str, tag: str, dockerfile: str = "Dockerfile") -> bool:
        """
        Build a Docker image from a Dockerfile.

        Args:
            path: Path to build context
            tag: Tag for the image
            dockerfile: Dockerfile name (default: Dockerfile)

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Building image '{tag}' from {path}...")
            image, build_logs = self.client.images.build(
                path=path,
                tag=tag,
                dockerfile=dockerfile,
                rm=True,  # Remove intermediate containers
                nocache=False
            )

            # Print build logs
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'], end='')

            print(f"\nSuccessfully built image: {tag}")
            return True
        except Exception as e:
            print(f"Error building image: {e}")
            return False

    def list_containers(self, all_containers: bool = False) -> List[Dict]:
        """
        List running or all Docker containers.

        Args:
            all_containers: If True, list all containers (running and stopped)

        Returns:
            List of container information
        """
        try:
            containers = self.client.containers.list(all=all_containers)
            container_list = []

            for container in containers:
                container_info = {
                    'id': container.id[:12],
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else 'N/A',
                    'ports': container.ports
                }
                container_list.append(container_info)

            return container_list
        except Exception as e:
            print(f"Error listing containers: {e}")
            return []

    def list_images(self) -> List[Dict]:
        """
        List all Docker images.

        Returns:
            List of image information
        """
        try:
            images = self.client.images.list()
            image_list = []

            for img in images:
                image_info = {
                    'id': img.id[:12],
                    'tags': img.tags,
                    'size': f"{img.attrs['Size'] / (1024*1024):.2f} MB",
                    'created': img.attrs['Created']
                }
                image_list.append(image_info)

            return image_list
        except Exception as e:
            print(f"Error listing images: {e}")
            return []

    def stop_container(self, container_id: str) -> bool:
        """
        Stop a running container.

        Args:
            container_id: ID or name of the container

        Returns:
            True if successful, False otherwise
        """
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            print(f"Successfully stopped container: {container_id}")
            return True
        except Exception as e:
            print(f"Error stopping container {container_id}: {e}")
            return False

    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """
        Remove a container.

        Args:
            container_id: ID or name of the container
            force: Force removal even if running

        Returns:
            True if successful, False otherwise
        """
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            print(f"Successfully removed container: {container_id}")
            return True
        except Exception as e:
            print(f"Error removing container {container_id}: {e}")
            return False

    def remove_image(self, image_id: str, force: bool = False) -> bool:
        """
        Remove a Docker image.

        Args:
            image_id: ID or name of the image
            force: Force removal even if in use

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.images.remove(image=image_id, force=force)
            print(f"Successfully removed image: {image_id}")
            return True
        except Exception as e:
            print(f"Error removing image {image_id}: {e}")
            return False

    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """
        Get logs from a container.

        Args:
            container_id: ID or name of the container
            tail: Number of lines to return from the end

        Returns:
            Container logs as string
        """
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail).decode('utf-8')
            return logs
        except Exception as e:
            print(f"Error getting logs from {container_id}: {e}")
            return ""

    def execute_command(self, container_id: str, command: str) -> Dict[str, Union[str, int]]:
        """
        Execute a command in a running container.

        Args:
            container_id: ID or name of the container
            command: Command to execute

        Returns:
            Dictionary with stdout, stderr, and exit_code
        """
        try:
            container = self.client.containers.get(container_id)
            result = container.exec_run(command)

            return {
                'stdout': result.output.decode('utf-8'),
                'stderr': '',
                'exit_code': result.exit_code
            }
        except Exception as e:
            print(f"Error executing command in {container_id}: {e}")
            return {'stdout': '', 'stderr': str(e), 'exit_code': -1}

    def create_network(self, name: str, driver: str = 'bridge') -> bool:
        """
        Create a Docker network.

        Args:
            name: Name of the network
            driver: Network driver (default: bridge)

        Returns:
            True if successful, False otherwise
        """
        try:
            network = self.client.networks.create(name=name, driver=driver)
            print(f"Successfully created network: {name}")
            return True
        except Exception as e:
            print(f"Error creating network {name}: {e}")
            return False

    def inspect_container(self, container_id: str) -> Dict:
        """
        Get detailed information about a container.

        Args:
            container_id: ID or name of the container

        Returns:
            Container details as dictionary
        """
        try:
            container = self.client.containers.get(container_id)
            return container.attrs
        except Exception as e:
            print(f"Error inspecting container {container_id}: {e}")
            return {}

    def cleanup_unused_resources(self) -> Dict[str, int]:
        """
        Clean up unused Docker resources (containers, images, networks, volumes).

        Returns:
            Dictionary with count of cleaned resources
        """
        try:
            # Remove stopped containers
            _, removed_containers = self.client.containers.prune()
            containers_count = len(removed_containers)

            # Remove unused images
            _, removed_images = self.client.images.prune(filters={'dangling': True})
            images_count = len(removed_images)

            # Remove unused networks
            _, removed_networks = self.client.networks.prune()
            networks_count = len(removed_networks)

            # Remove unused volumes
            _, removed_volumes = self.client.volumes.prune()
            volumes_count = len(removed_volumes)

            result = {
                'containers': containers_count,
                'images': images_count,
                'networks': networks_count,
                'volumes': volumes_count
            }

            print("Cleanup completed:")
            print(f"  Removed {containers_count} containers")
            print(f"  Removed {images_count} images")
            print(f"  Removed {networks_count} networks")
            print(f"  Removed {volumes_count} volumes")

            return result
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return {}


def check_docker_installation() -> bool:
    """
    Check if Docker is installed and running.

    Returns:
        True if Docker is accessible, False otherwise
    """
    try:
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"Docker version: {result.stdout.strip()}")
            return True
        else:
            print("Docker is not installed or not accessible.")
            return False
    except FileNotFoundError:
        print("Docker command not found. Please install Docker.")
        return False
    except subprocess.TimeoutExpired:
        print("Docker command timed out. Please check if Docker daemon is running.")
        return False
    except Exception as e:
        print(f"Error checking Docker installation: {e}")
        return False


def generate_dockerfile_suggestions(context_dir: str = ".") -> List[str]:
    """
    Generate Dockerfile suggestions based on files in the context directory.

    Args:
        context_dir: Directory to analyze for Dockerfile suggestions

    Returns:
        List of suggested Dockerfile improvements
    """
    suggestions = []
    path = Path(context_dir)

    # Check for common application files
    if path.joinpath("requirements.txt").exists():
        suggestions.append("Detected Python application - consider using python:3.x-slim as base image")

    if path.joinpath("package.json").exists():
        suggestions.append("Detected Node.js application - consider using node:xx-alpine as base image")

    if path.joinpath("go.mod").exists():
        suggestions.append("Detected Go application - consider using multi-stage build with golang and alpine")

    if path.joinpath("pom.xml").exists() or path.joinpath("build.gradle").exists():
        suggestions.append("Detected Java application - consider using openjdk:xx-jre-slim as base image")

    # Check for common security issues
    dockerfile_path = path.joinpath("Dockerfile")
    if dockerfile_path.exists():
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read().lower()

        if 'from ubuntu' in dockerfile_content or 'from centos' in dockerfile_content:
            suggestions.append("Consider using smaller base images like alpine or distroless for reduced attack surface")

        if 'run apt-get update && apt-get install' in dockerfile_content and 'apt-get clean' not in dockerfile_content:
            suggestions.append("Remember to run 'apt-get clean' and 'rm -rf /var/lib/apt/lists/*' to reduce image size")

        if 'user root' in dockerfile_content or 'user 0' in dockerfile_content:
            suggestions.append("Consider running as non-root user for security: create and use a dedicated user")

    return suggestions


def get_docker_system_info() -> Dict:
    """
    Get Docker system information.

    Returns:
        Dictionary with Docker system information
    """
    try:
        client = docker.from_env()
        info = client.info()

        return {
            'server_version': info.get('ServerVersion', 'Unknown'),
            'storage_driver': info.get('Driver', 'Unknown'),
            'docker_root_dir': info.get('DockerRootDir', 'Unknown'),
            'containers': info.get('Containers', 0),
            'running_containers': info.get('ContainersRunning', 0),
            'paused_containers': info.get('ContainersPaused', 0),
            'stopped_containers': info.get('ContainersStopped', 0),
            'images': info.get('Images', 0),
            'operating_system': info.get('OperatingSystem', 'Unknown'),
            'architecture': info.get('Architecture', 'Unknown'),
            'cpus': info.get('NCPU', 0),
            'memory': f"{info.get('MemTotal', 0) / (1024**3):.2f} GB"
        }
    except Exception as e:
        print(f"Error getting Docker system info: {e}")
        return {}


def main():
    """
    Main function to demonstrate Docker helper capabilities.
    """
    print("Docker Helper Utility")
    print("=" * 30)

    # Check Docker installation
    if not check_docker_installation():
        print("Please install Docker and ensure it's running before proceeding.")
        return

    # Initialize Docker helper
    docker_helper = DockerHelper()

    # Display system information
    print("\nDocker System Information:")
    system_info = get_docker_system_info()
    for key, value in system_info.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    # Example operations
    print("\nExample operations available:")
    print("  - List containers: docker_helper.list_containers()")
    print("  - List images: docker_helper.list_images()")
    print("  - Build image: docker_helper.build_image(path, tag)")
    print("  - Run container: docker_helper.run_container(image)")
    print("  - Cleanup resources: docker_helper.cleanup_unused_resources()")

    # Generate Dockerfile suggestions if applicable
    suggestions = generate_dockerfile_suggestions()
    if suggestions:
        print(f"\nDockerfile Suggestions for current directory:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")


if __name__ == "__main__":
    main()
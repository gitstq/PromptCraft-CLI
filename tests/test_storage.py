"""
Tests for PromptStorage
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from promptcraft.storage import PromptStorage


class TestPromptStorage(unittest.TestCase):
    """Test cases for PromptStorage"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PromptStorage(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_project(self):
        """Test project creation"""
        project = self.storage.create_project("Test Project", "A test project")
        
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "A test project")
        self.assertEqual(len(project.versions), 0)
    
    def test_add_version(self):
        """Test adding version to project"""
        project = self.storage.create_project("Test")
        version = self.storage.add_version(
            project.id,
            "Test prompt content",
            description="Initial version",
            tags=["test", "v1"]
        )
        
        self.assertIsNotNone(version)
        self.assertEqual(version.content, "Test prompt content")
        self.assertEqual(version.description, "Initial version")
    
    def test_get_project(self):
        """Test retrieving project"""
        created = self.storage.create_project("Test")
        retrieved = self.storage.get_project(created.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, created.name)
    
    def test_list_projects(self):
        """Test listing projects"""
        self.storage.create_project("Project 1")
        self.storage.create_project("Project 2")
        
        projects = self.storage.list_projects()
        self.assertEqual(len(projects), 2)
    
    def test_delete_project(self):
        """Test project deletion"""
        project = self.storage.create_project("To Delete")
        result = self.storage.delete_project(project.id)
        
        self.assertTrue(result)
        self.assertIsNone(self.storage.get_project(project.id))
    
    def test_export_project(self):
        """Test project export"""
        project = self.storage.create_project("Export Test")
        self.storage.add_version(project.id, "Test content")
        
        json_export = self.storage.export_project(project.id, "json")
        self.assertIsNotNone(json_export)
        
        md_export = self.storage.export_project(project.id, "markdown")
        self.assertIsNotNone(md_export)
        self.assertIn("# Export Test", md_export)


if __name__ == '__main__':
    unittest.main()

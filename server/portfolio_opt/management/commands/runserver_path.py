import os
from django.core.management.commands.runserver import Command as BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs the development server with a file path parameter'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--file_path', type=str, help='The path to the file containing returns data')
        parser.add_argument('--rank_file_path', type=str, help='The path to the rank file')
        parser.add_argument('--comment_file_path', type=str, help='The path to the comment')
        parser.add_argument('--port', type=int, default=8000, help='The port to run the server on')
        parser.add_argument('--host', type=str, default='127.0.0.1', help='The host to run the server on')

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        if file_path:
            # Set the file path in Django settings
            settings.RETURNS_DATA_FILE_PATH = file_path

        # Call the base command's handle method
        super().handle(*args, **options)
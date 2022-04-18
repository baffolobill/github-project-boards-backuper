import logging
import json
import sys
from pathlib import Path

import click
from github import Github


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


@click.command()
@click.option('--user', help='Your GitHub Username.')
@click.option('--token', help='Your GitHub Personal Access Token.')
@click.option('--output-directory', help='Directory at which to backup.')
def main(user, token, output_directory):
    output_directory = Path(output_directory)
    if not output_directory.exists():
        output_directory.mkdir(exist_ok=True, parents=True)

    github_handler = Github(token)
    for repo in github_handler.get_user().get_repos(type='private'):
        try:
            for project in repo.get_projects():
                project_backup_dir = output_directory / repo.name
                project_backup_dir.mkdir(exist_ok=True, parents=True)
                project_backup_file = project_backup_dir / f'{project.id}_{project.name}.json'

                project_dump = project.raw_data.copy()
                project_dump['columns'] = []

                for column in project.get_columns():
                    column_dump = column.raw_data.copy()
                    column_dump['cards'] = []

                    for card in column.get_cards():
                        card_dump = card.raw_data.copy()
                        
                        # Dump linked Issue or PullRequest.
                        card_dump['content'] = None
                        card_content = card.get_content()
                        if card_content:
                            card_dump['content'] = card_content.raw_data
                        
                        column_dump['cards'].append(card_dump)

                    project_dump['columns'].append(column_dump)
                
                with project_backup_file.open('w') as fp:
                    json.dump(project_dump, fp)

        except Exception:
            logger.exception(
                "Couldn't fetch Repo (id:%s name:%s) Projects.", 
                repo.id,
                repo.name,
            )


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Couldn't perform backup.")
        sys.exit(1)

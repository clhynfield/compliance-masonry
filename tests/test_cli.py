""" Integration tests for Control Masonry CLI """

import glob
import os
import yaml
import pytest
import tempfile

from click.testing import CliRunner
from src import cli


@pytest.fixture
def runner():
    return CliRunner()

# Data directories
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
EXPORTS_DATA_DIR = os.path.join(DATA_DIR, 'exports')
DOCS_DATA_DIR = os.path.join(DATA_DIR, 'docs')
INVENT_DATA_DIR = os.path.join(DATA_DIR, 'inventory')

# Output directories
TEMP_OUTPUT_DIR = tempfile.TemporaryDirectory()
CERTS_OUTPUT_DIR = os.path.join(TEMP_OUTPUT_DIR.name, 'certifications')
DOCS_OUTPUT_DIR = os.path.join(TEMP_OUTPUT_DIR.name, 'docs')
COMPS_OUTPUT_DIR = os.path.join(TEMP_OUTPUT_DIR.name, 'components')
INVENT_OUTPUT_DIR = os.path.join(TEMP_OUTPUT_DIR.name, 'inventory')


def load_file(file_path):
    with open(file_path, 'r') as file_content:
        return file_content.read()


def load_yaml_file(yaml_path):
    with open(yaml_path, 'r') as yaml_file:
        data = yaml.load(yaml_file)
    return data


def test_certs_run(runner):
    """ Check that certs command runs properly """
    result = runner.invoke(
        cli.main,
        ['certs', 'LATO', '-d{0}'.format(DATA_DIR), '-o{0}'.format(CERTS_OUTPUT_DIR)]
    )
    output = 'Certification created in: `{0}`'.format(CERTS_OUTPUT_DIR)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == output


def test_certs_yaml(runner):
    """ Check that the certification files were created properly """
    CERTS_DATA_DIR = os.path.join(EXPORTS_DATA_DIR, 'certifications')
    for expected_file_path in glob.iglob(os.path.join(CERTS_DATA_DIR, '*/*/*')):
        generated_file_path = expected_file_path.replace(CERTS_DATA_DIR, CERTS_OUTPUT_DIR)
        assert os.path.exists(generated_file_path)

    certs_yaml_file = os.path.join(CERTS_OUTPUT_DIR, 'LATO.yaml')
    generated_yaml = load_yaml_file(certs_yaml_file)
    expected_yaml = load_yaml_file(os.path.join(DATA_DIR, 'exports/certifications/LATO.yaml'))
    assert generated_yaml == expected_yaml


def test_inventory_builder(runner):
    result = runner.invoke(
        cli.main,
        [
            'inventory',
            '-e{0}'.format(EXPORTS_DATA_DIR),
            '-o{0}'.format(INVENT_OUTPUT_DIR),
            'LATO',
        ]
    )
    output = 'Inventory yaml created at `{0}`'.format(
        os.path.join(INVENT_OUTPUT_DIR, 'LATO.yaml')
    )
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == output


def test_inventory_builder_yaml_output(runner):
    """ Check that the certification that was created has the correct
    attributes """
    certs_yaml_file = os.path.join(INVENT_OUTPUT_DIR, 'LATO.yaml')
    generated_yaml = load_yaml_file(certs_yaml_file)
    expected_yaml = load_yaml_file(
        os.path.join(INVENT_DATA_DIR, 'LATO.yaml')
    )
    assert generated_yaml == expected_yaml


def test_gitbook_runs(runner):
    """ Check that the gitbook command is runs properly """
    result = runner.invoke(
        cli.main,
        [
            'docs', 'gitbook', 'LATO',
            '-e{0}'.format(EXPORTS_DATA_DIR),
            '-d{0}'.format(DATA_DIR),
            '-o{0}'.format(DOCS_OUTPUT_DIR)
        ]
    )
    output = 'Gitbook Files Created in `{0}`'.format(os.path.join(DOCS_OUTPUT_DIR, 'gitbook'))
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == output


def test_gitbook_files(runner):
    """ Check that the gitbook files were created properly """
    glob_path = os.path.join(DOCS_DATA_DIR, '*/*.md')
    for expected_file_path in glob.iglob(glob_path):
        generated_file_path = expected_file_path.replace(DOCS_DATA_DIR, DOCS_OUTPUT_DIR)
        assert os.path.exists(generated_file_path)
        assert load_file(generated_file_path) == load_file(expected_file_path)


def test_gitbook_catches_unsupported_type_error(runner):
    """ Check that the gitbook command is runs properly """
    result = runner.invoke(
        cli.main,
        [
            'docs', 'gitbooc', 'LATO',
            '-e{0}'.format(EXPORTS_DATA_DIR),
            '-o{0}'.format(DOCS_OUTPUT_DIR)
        ]
    )
    assert result.output.strip() == "gitbooc format is not supported yet..."


def test_new_system_runs(runner):
    """ Check that the new component command is runs properly """
    result = runner.invoke(
        cli.main,
        [
            'new', 'system', 'testsystem',
            '-d{0}'.format(COMPS_OUTPUT_DIR)
        ]
    )
    output = 'New System: `{0}`'.format(
        os.path.join(
            COMPS_OUTPUT_DIR, 'components', 'testsystem', 'system.yaml'
        )
    )
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == output


def test_new_system_yaml(runner):
    """ Check that the certification that was created has the correct
    attributes """
    comp_yaml_file = os.path.join(
        COMPS_OUTPUT_DIR, 'components', 'testsystem', 'system.yaml'
    )
    generated_yaml = load_yaml_file(comp_yaml_file)
    expected_yaml = load_yaml_file(
        os.path.join(
            DATA_DIR, 'testnewcomponent', 'components', 'testsystem', 'system.yaml'
        )
    )
    assert generated_yaml == expected_yaml


def test_new_component_runs(runner):
    """ Check that the new component command is runs properly """
    result = runner.invoke(
        cli.main,
        [
            'new', 'component', 'testsystem', 'testcomponent',
            '-d{0}'.format(COMPS_OUTPUT_DIR)
        ]
    )
    output = 'New Component: `{0}`'.format(
        os.path.join(
            COMPS_OUTPUT_DIR, 'components', 'testsystem',
            'testcomponent', 'component.yaml'
        )
    )
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == output


def test_new_component_yaml(runner):
    """ Check that the certification that was created has the correct
    attributes """
    comp_yaml_file = os.path.join(
        COMPS_OUTPUT_DIR, 'components', 'testsystem',
        'testcomponent', 'component.yaml'
    )
    generated_yaml = load_yaml_file(comp_yaml_file)
    expected_yaml = load_yaml_file(
        os.path.join(
            DATA_DIR, 'testnewcomponent', 'components', 'testsystem',
            'testcomponent', 'component.yaml'
        )
    )
    assert generated_yaml == expected_yaml


TEMP_OUTPUT_DIR.cleanup()
import click

from command.output import CliOutput
from api.client import ApiClient
from api.firmware import Firmware

pass_api_client = click.make_pass_decorator(ApiClient)
pass_firmware_svc = click.make_pass_decorator(Firmware)

@click.group()
@pass_api_client
@click.pass_context
def plugin(ctx, api_client: ApiClient, **kwargs):
    ctx.obj = Firmware(api_client)

@plugin.command()
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="name,version,comment,installed",
    show_default=True,
)
@pass_firmware_svc
def list(firmware_svc: Firmware, **kwargs):
    """
    Show all available plugins.
    """
    result = firmware_svc.info()['plugin']

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="name,version,comment,locked",
    show_default=True,
)
@pass_firmware_svc
def installed(firmware_svc : Firmware, **kwargs):
    """
    Show installed plugins.
    """
    plugins = firmware_svc.info()['plugin']
    result = [plugin for plugin in plugins if plugin['installed'] == "1"]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="details",
    show_default=True,
)
@pass_firmware_svc
def show(firmware_svc : Firmware, **kwargs):
    """
    Show plugin details.
    """
    result = [firmware_svc.details(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="status",
    show_default=True,
)
@pass_firmware_svc
def install(firmware_svc : Firmware, **kwargs):
    """
    Install plugin by name
    """
    result = [firmware_svc.install(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="status",
    show_default=True,
)
@pass_firmware_svc
def uninstall(firmware_svc : Firmware, **kwargs):
    """
    Uninstall plugin by name.
    """
    result = [firmware_svc.remove(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()

@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="status",
    show_default=True,
)
@pass_firmware_svc
def reinstall(firmware_svc : Firmware, **kwargs):
    """
    Reinstall plugin by name.
    """
    result = [firmware_svc.reinstall(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()

@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="status",
    show_default=True,
)
@pass_firmware_svc
def lock(firmware_svc : Firmware, **kwargs):
    """
    Lock plugin.
    """
    result = [firmware_svc.lock(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()


@plugin.command()
@click.argument('plugin_name')
@click.option(
    '--output', '-o',
    help='Specifies the output format.',
    default="table",
    type=click.Choice(['table', 'json']),
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed?',
    default="status",
    show_default=True,
)
@pass_firmware_svc
def unlock(firmware_svc : Firmware, **kwargs):
    """
    Unlock plugin.
    """
    result = [firmware_svc.unlock(kwargs['plugin_name'])]

    CliOutput(result, kwargs['output'], kwargs['cols'].split(",")).echo()










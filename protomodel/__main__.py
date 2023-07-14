import click
import  importlib.util

@click.group()
def cli():
    pass

@cli.command()
@click.option('--python_file', help='Python file name with directory.')
@click.option('--proto_name', help='Proto buffer file name with directory.')
def generate(python_file, proto_name):
    from protomodel import message, service
    from typing import TextIO, List

    input_filename = python_file
    output_filename = proto_name
    package_name = "app.proto"

    data_spec = importlib.util.spec_from_file_location(input_filename.split(".")[0], input_filename)
    data_module = importlib.util.module_from_spec(data_spec)
    data_spec.loader.exec_module(data_module)

    proto_file: TextIO = open(f"{output_filename}", "w")
    proto_file.write(f'syntax = "proto3";\n\npackage {package_name};\n\n')

    messages: List[message] = [cls for cls in data_module.__dict__.values() if isinstance(cls, message)]
    services: List[service] = [cls for cls in data_module.__dict__.values() if isinstance(cls, service)]

    for msg in messages:
        msg.add_field(proto_file)

    for service in services:
        service.add_field(proto_file)

    print('file created.')
    proto_file.close()

if __name__ == "__main__":
    cli()
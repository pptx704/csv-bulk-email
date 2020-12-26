import click
import os
from .extras import gmailvars, template_message
from .mailer import TextMail

# creating default files
def defaultmaker(type="a"):
    # create env
    with open(".env", type) as env:
        env.writelines(gmailvars)

    # create blank template
    with open("template.txt", "w") as template:
        template.write(template_message)


@click.group()
def main():
    pass


@main.command()
def defaults():
    """Creates basic files for you"""
    defaultmaker()
    click.echo("Created default files.")


@main.command()
@click.option(
    "--database",
    "--d",
    type=str,
    prompt=True,
    help="database filename e.g. 'database.csv'",
)
@click.option(
    "--type",
    type=str,
    required=False,
    default="plain",
    help="Email body type. Must be 'plain' or 'html'",
    show_default=True,
)
@click.option(
    "--template",
    "--t",
    type=str,
    prompt=True,
    help="Template file name e.g. 'template.txt'",
)
@click.option("--subject", "--s", type=str, prompt=True, help="Subject of your email.")
@click.option(
    "--email-field", "--e", type=str, prompt=True, help="Email Field name in CSV file"
)
def sendmail(database, type, template, subject, email_field):
    """Send emails using the locally saved files"""
    mail = TextMail(database, type, template, email_field, subject)
    if click.confirm("Do you want to use variables?"):
        variables = dict()
        for i in range(click.prompt("Number of variable fields", type=int)):
            click.echo(f"Variable no. {i+1}")
            varname = click.prompt("Variable Name")
            varfield = click.prompt("Fieldname")
            variables[varname] = varfield
        mail.add_variables(variables)
    click.echo(
        "Started sending emails. Please check success.log and failure.log for updates on individual emails"
    )
    mail.send()
    click.echo("Sending complete.")


@main.command()
@click.option(
    "--database",
    "--d",
    type=str,
    prompt=True,
    help="database filename e.g. 'database.csv'",
)
@click.option(
    "--subject", "--s", type=str, prompt=True, help="Subject of your email."
)
@click.option(
    "--email-field", "--e", type=str, prompt=True, help="Email Field name in CSV file"
)
def sendtemp(database, subject, email_field):
    """This command will use temporary files for database and will delete those after sending the emails. Only the log files will remain"""
    type = click.prompt("Email body type (plain or html)")
    defaultmaker("w")
    click.echo("Edit the template.txt and .env file and then continue.")
    if click.confirm("Are you done editing the files?"):
        mail = TextMail(
            filename=database,
            template="template.txt",
            type=type,
            email_field=email_field,
            subject=subject,
        )
        if click.confirm("Do you want to use variables?"):
            variables = dict()
            for i in range(click.prompt("Number of variable fields", type=int)):
                click.echo(f"Variable no. {i+1}")
                varname = click.prompt("Variable Name")
                varfield = click.prompt("Fieldname")
                variables[varname] = varfield
            mail.add_variables(variables)
        click.echo(
            "Started sending emails. Please check success.log and failure.log for updates on individual emails"
        )
        mail.send()
        click.echo("Sending complete.")
    os.remove(".env")
    os.remove("template.txt")

from celery.decorators import task


@task
def handle_mail(mail_dict):
    # Todo: check and save
    pass
    
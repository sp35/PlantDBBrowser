from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Gene
from .helpers import send_email


@receiver(post_save, sender=Gene)
def active(sender, instance: Gene, created, **kwargs):
    if created:
        species_name = "-"
        contributor = "-"
        if instance.species is not None:
            species_name = instance.species.name
        if instance.linked_suggestion is not None:
            contributor = f"{instance.linked_suggestion.contributor_name} ({instance.linked_suggestion.contributor_email})"
        subject = 'Dream Database: New Entry Received'
        content_html = """
        <table>
            <tr>
                <th>Gene Name</th>
                <th>Plant Species</th>
                <th>Submitted by</th>
            </tr>
            <tr>
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
            </tr>
        </table>
        """.format(instance.name, species_name, contributor)
        send_email(subject=subject, html=content_html)
 
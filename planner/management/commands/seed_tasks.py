from django.core.management.base import BaseCommand
from faker import Faker
import random
from planner.models import Vault_Goal, Micro_task, ThreatLevel
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with fake Vault Goals and Micro Tasks"

    def handle(self, *args, **kwargs):

        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("No users found. Create a user first."))
            return

        # --- Create Vault Goals ---
        goals = []
        for _ in range(5):
            goal = Vault_Goal.objects.create(
                user=random.choice(users),
                title=fake.sentence(nb_words=3),
                is_active=random.choice([True, False]),
                soft_deadline=fake.date_time_between(start_date="now", end_date="+10d")
            )
            goals.append(goal)

        # --- Create Micro Tasks ---
        threats = [choice[0] for choice in ThreatLevel.choices]   # adjust to your actual choices

        for _ in range(20):
            Micro_task.objects.create(
                parent_goal=random.choice(goals),
                title=fake.sentence(nb_words=4),
                threat=random.choice(threats),
                skip_count=random.randint(0, 5),
                status=random.choice([s[0] for s in Micro_task.STATUS_CHOICES]),
                
            )

        self.stdout.write(self.style.SUCCESS("✅ Fake data generated successfully!"))
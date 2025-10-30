# File: mini_insta/models.py
# Author: María Díaz Garrido
# Description: Database models for the voter_analytics app.

from django.db import models
from django.urls import reverse

# Create your models here.

class Voter(models.Model):
    """Registered voter in Newton, MA."""
    last_name = models.TextField(blank=True)
    first_name = models.TextField(blank=True)

    res_street_number = models.CharField(max_length=16, blank=True)
    res_street_name = models.TextField(blank=True)
    res_apartment = models.CharField(max_length=32, blank=True)
    res_zip = models.CharField(max_length=10, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party = models.CharField(max_length=2, blank=True)    
    precinct = models.CharField(max_length=8, blank=True)

    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} at zip code {self.res_zip} with a voter score of {self.voter_score}'
    
    
    def load_data():
        '''Function to load data records from CSV file into Django model instances.'''
        
        Voter.objects.all().delete()

        filename = "/Users/Maria/Downloads/newton_voters.csv"
        f = open(filename)
        f.readline() 
    
        for line in f:
            fields = line.split(',')
            try:
                result = Voter(last_name=fields[1],
                                first_name=fields[2],
                                res_street_num = fields[3],
                                res_street_name = fields[4],
                                res_apt_num = fields[5],
                                res_zip = fields[6],
                                
                                dob = fields[7],
                                dor = fields[8],
                                party_affiliation = fields[9],
                                precinct_num = fields[10],
                            
                                v20state = fields[11],
                                v21town = fields[12],
                                v21primary = fields[13],
                                v22general = fields[14],
                                v23town = fields[15],
                                voter_score = fields[16],
                            )

                result.save() 
                print(f'Created result: {result}')
            except:
                print(f"Skipped: {fields}")
        
        print(f'Done. Created {len(Voter.objects.all())}.')
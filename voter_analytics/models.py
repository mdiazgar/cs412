# File: mini_insta/models.py
# Author: María Díaz Garrido
# Description: Database models for the voter_analytics app.

from django.db import models
from django.urls import reverse
from datetime import datetime


# Create your models here.

from django.db import models
import csv
from datetime import date

# Create your models here.

class Voter(models.Model):
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    
    address_street_number = models.CharField(max_length=16, blank=True, null=True)  
    address_street_name = models.TextField(blank=True)
    address_apartment_number = models.CharField(max_length=16, blank=True, null=True)  
    address_zip_code = models.CharField(max_length=10, blank=True, null=True)  
    
    date_birth = models.DateField(blank=True, null=True)
    date_registration = models.DateField(blank=True, null=True)
    
    party = models.CharField(max_length=2, blank=True, null=True)
    precinct_number = models.CharField(max_length=10, blank=True, null=True)
    
    v20state = models.IntegerField(blank=True, null=True)
    v21town = models.IntegerField(blank=True, null=True)
    v21primary = models.IntegerField(blank=True, null=True)
    v22general = models.IntegerField(blank=True, null=True)
    v23town = models.IntegerField(blank=True, null=True)
    
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        apt = f" Apt {self.address_apartment_number}" if self.address_apartment_number is not None else ""
        return (
            f"Full name: {self.first_name} {self.last_name}, "
            f"Date of Birth: {self.date_birth}, "
            f"Address: {self.address_street_number} {self.address_street_name}{apt}, "
            f"Zip: {self.address_zip_code}, Party: {self.party}"
        )


def load_data():
    """Function to load data records from CSV file into Django model instances."""
    filename = "/Users/Maria/Desktop/MARTIN/CS 412/django/newton_voters.csv"

    def to_int_strict(s):
        if s in (None, "", "NULL", "None"):
            return None
        s = str(s).strip()
        return int(s) if s.isdigit() else None 

    def to_date(s):
        if s in (None, "", "NULL", "None"):
            return None
        s = str(s).strip()
        from datetime import date, datetime
        try:
            return date.fromisoformat(s)
        except Exception:
            pass
        for fmt in ("%m/%d/%y %H:%M", "%m/%d/%y", "%m/%d/%Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except Exception:
                continue
        return None

    def to_bool_int(s):
        if s is None:
            return None
        s_up = str(s).strip().upper()
        if s_up in ("TRUE", "T", "1", "YES", "Y"):
            return 1
        if s_up in ("FALSE", "F", "0", "NO", "N", ""):
            return 0
        return None

    def clean_party(s):
        if s in (None, "", "NULL", "None"):
            return None
        return s.strip().upper()[:1] 
    
    def keep_str(s):
        s = (s or "").strip()
        return s or None

    def keep_zip(s):
        s = (s or "").strip()
        if s.isdigit():          
            return s.zfill(5)
        return s or None


    batch, created = [], 0
    BATCH_SIZE = 2000

    import csv
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None) 

        for lineno, line in enumerate(reader, start=2):  
            try:
                voter = Voter(
                    last_name=line[1].strip() if len(line) > 1 else "",
                    first_name=line[2].strip() if len(line) > 2 else "",
                    address_street_number = keep_str(line[3]) if len(line) > 3 else None,
                    address_street_name = keep_str(line[4]) if len(line) > 4 else None,
                    address_apartment_number = keep_str(line[5]) if len(line) > 5 else None,
                    address_zip_code = keep_zip(line[6]) if len(line) > 6 else None,
                    date_birth=to_date(line[7]) if len(line) > 7 else None,
                    date_registration=to_date(line[8]) if len(line) > 8 else None,
                    party=clean_party(line[9]) if len(line) > 9 else None,
                    precinct_number=(line[10].strip() or None) if len(line) > 10 else None,
                    v20state=to_bool_int(line[11]) if len(line) > 11 else None,
                    v21town=to_bool_int(line[12]) if len(line) > 12 else None,
                    v21primary=to_bool_int(line[13]) if len(line) > 13 else None,
                    v22general=to_bool_int(line[14]) if len(line) > 14 else None,
                    v23town=to_bool_int(line[15]) if len(line) > 15 else None,
                    voter_score=to_int_strict(line[16]) if len(line) > 16 else 0,
                )
                batch.append(voter)

                if len(batch) >= BATCH_SIZE:
                    Voter.objects.bulk_create(batch, ignore_conflicts=False)
                    created += len(batch)
                    batch.clear()

            except Exception as e:
                print(f"[load_data] error on CSV line {lineno}: {e}")
                print(f"line={line}")

    if batch:
        Voter.objects.bulk_create(batch, ignore_conflicts=False)
        created += len(batch)

    print(f"Created {created} Voters (total now {Voter.objects.count()})")

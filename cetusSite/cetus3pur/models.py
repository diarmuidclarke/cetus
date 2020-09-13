from django.db import models


# A 3rd party, e.g. belcan UK
class ThirdParty(models.Model):
    legal_entity_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
            return self.legal_entity_name + ' [loc:' + self.location + ']'




# A 3rd party employee
class ThirdPartyUser(models.Model):
    firstname = models.CharField(max_length=50)
    familyname = models.CharField(max_length=50)
    employer = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)
    userac_name = models.CharField(max_length=10)
    userac_expirydate = models.DateField('Expiry date')

    @classmethod
    def create(cls, nfirstname, nfamilyname, nemployee_id, nuserac, nuseracexp , nemployer_id):
        tpu = cls(firstname=nfirstname, familyname = nfamilyname, employee_id = nemployee_id, userac_name = nuserac, userac_expirydate = nuseracexp, employer =  ThirdParty.objects.get(pk = nemployer_id))
        return tpu

    def __str__(self):
            return (self.firstname + ' @ ' + self.employer.legal_entity_name + " at location " + self.employer.location)




# R=R Responsible Manager
class RRResponsibleManager(models.Model):
    firstname = models.CharField(max_length=50)
    familyname = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20)
    user_ac =  models.CharField(max_length=10, default='<null>')
    
    def __str__(self):
            return self.firstname + ' @ R-R'


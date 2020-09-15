from django.db import models


# A 3rd party, e.g. belcan UK
class ThirdParty(models.Model):
    legal_entity_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    class Meta:
        verbose_name = "3P Business"
        verbose_name_plural = "3P Businesses"

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

    class Meta:
        verbose_name = "3P User"
        verbose_name_plural = "3P Users"

    def __str__(self):
            return (self.firstname + ' @ ' + self.employer.legal_entity_name + " at location " + self.employer.location)




# R=R Responsible Manager
class RRResponsibleManager(models.Model):
    firstname = models.CharField(max_length=50)
    familyname = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20)
    user_ac =  models.CharField(max_length=10, default='<null>')
    
    class Meta:
        verbose_name = "R-R Responsible Manager"
        verbose_name_plural = "R-R Responsible Managers"

    def __str__(self):
            return self.firstname + ' @ R-R'



## EAB Request
class EAB_Request(models.Model):
    date = models.DateField('Date of Req.')
    reqstr_userid = models.CharField('Requester User ID', max_length=10)
    tp = models.ForeignKey( ThirdParty, on_delete=models.CASCADE)
    data_store = models.CharField( 'Date Store', max_length=256)
    data_owner_userid =  models.CharField( 'Data Owner User ID', max_length=10)
    data_store_export_claim = models.CharField('Export status of Data Store', max_length=512 )
    ipecr = models.IntegerField('IPECR #')
    
    class Meta:
        verbose_name = "EAB Request"
        verbose_name_plural = "EAB Requests"

    def __str__(self):
            return self.reqstr_userid + ' req for ' + str(self.tp) + ' access to ' + self.data_store


## EAB Approval
class EAB_Approval(models.Model):
    request = models.ForeignKey(EAB_Request, on_delete=models.CASCADE, default = None)
    date = models.DateField('Date of Review.')
    approver_userid = models.CharField('Approver User ID',max_length=10)
    decision =  models.CharField('Decision', max_length=3, choices = [ ('APP','Approved'),('REJ','Rejected'),('PEN','Pending')])
    ecm_comment = models.CharField('ECM comment' , max_length=512) # Export Control Manager
    ipm_comment = models.CharField('IP Manager comment', max_length=512) # IP manager
    IT_comment = models.CharField('IT Comment', max_length=512) # IT comment

    class Meta:
        verbose_name = "EAB Approval"
        verbose_name_plural = "EAB Approvals"

    def __str__(self):
            return self.approver_userid + ' reviewed as ' + self.decision + ' on ' + str(self.date)

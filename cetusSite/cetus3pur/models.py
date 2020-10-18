from django.db import models
from django.core.exceptions import ValidationError
from .validators import validateUserName



# A 3rd party, e.g. belcan UK
class ThirdParty(models.Model):
    legal_entity_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    ad_group_name = models.CharField('AD Group Name', max_length=50, default='AD group todo')
    
    class Meta:
        verbose_name = "3P Business"
        verbose_name_plural = "3P Businesses"

    def __str__(self):
            return self.legal_entity_name + ' [' + self.location + ']'





# A 3rd party employee
class ThirdPartyUser(models.Model):
    firstname = models.CharField('First name', max_length=50)
    familyname = models.CharField('Family name', max_length=50)
    employer = models.ForeignKey(ThirdParty, on_delete=models.CASCADE)
    employee_id = models.CharField('3P Employee ID', max_length=20)
    userac_name = models.CharField('User account name', max_length=10)
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









# what datastore is the requestor seeking to share
# implications for approvals, also useful for impact analysis
class EAB_DataStoreSystem(models.Model):
    DATASTORESYSTEM_CHOICES = [
        ('RRCS_APPROVED_CHANNEL',  'Approved Channel'),
        ('RRCS_NOT_APPROVED_CHANNEL',    'Not Approved as a Channel for Export Controlled data'),
    ]

    name = models.CharField(
        'Data Store System name',
        max_length=100,
        default = 'tbd',
    )


    # to store the selection from the standard list of data store systems
    datastoresystem_approved = models.CharField(
        'Data store system channel status',
        max_length=30,
        choices=DATASTORESYSTEM_CHOICES,
        default='RRCS_OTHER',
    )


    class Meta:
        verbose_name = "Data Store System"
        verbose_name_plural = "Data Store System"

    def __str__(self):
        return (self.name)




# A sub-folder, or partition within the data store system which is intended for a particular classification of data
class EAB_DataStoreSystemArea(models.Model):
    name = models.CharField(
        'Area name',
        max_length=100,
        default = 'tbd',
    )

    dss = models.ForeignKey(
        EAB_DataStoreSystem, 
        related_name='dss_areas',
        on_delete=models.CASCADE
    )


    export_classification_PL9009c = models.BooleanField(
        'Intended to contain PL9009.c',
        default=False,
    )

    export_classification_EU_dualuse = models.BooleanField(
        'Intended to contain EU Dual Use',
        default=False,
    )

    export_classification_US_NLR = models.BooleanField(
        'Intended to contain US NLR (no license required)',
        default=False,
    )

    class Meta:
        verbose_name = "Data storage system Area"
        verbose_name_plural = "Data storage system Areas"

    def __str__(self):
            return ' [area:' + self.name + ']'




## EAB Request
class EAB_Request(models.Model):
    date = models.DateField(
        verbose_name = 'Date',
        help_text = 'Date of this EAB request'
    )

    reqstr_userid = models.CharField(
        verbose_name = 'Requester User ID',
        help_text = 'User ID of person making the request',
        max_length=10,
    )

    tp = models.ForeignKey(
        ThirdParty,
        help_text = 'Name and location must be correct',
        verbose_name = 'Third Party',
        related_name='third_party',
        on_delete=models.CASCADE,
    )

    # e.g. integrity, artisan, nas drive
    data_store_system = models.ForeignKey(
        EAB_DataStoreSystem,
        help_text='The IT System that holds the data',
        related_name='data_store_system',
        on_delete=models.CASCADE,
        null=True
    )  # todo : check this use of related_name



    # e.g. T7000 project in Integrity
    data_store_system_area = models.ForeignKey(
        EAB_DataStoreSystemArea,
        help_text='A reposotory, subfolder, or other part of the IT System, which is to be exported (shared with a 3rd party)',
        related_name='data_store_system_area',
        on_delete=models.CASCADE,
        null=True
    )



    # owner of that part of the data store system, e.g. owner of a specific network folder
    data_owner_userid =  models.CharField(
        'Data Owner User ID',
        help_text = 'User ID of the person who owns this data store',
        max_length=10
    )



    # ipecr - if known/needed
    ipecr = models.IntegerField(
        'IPECR #',
        help_text = 'A six digit number, or use 0 if unsure',
        blank = True,
        default=0,
    )





    @classmethod
    def create(cls, ndate, nrqsteruid, ntpid, ndatastore_system, ndatastore_system_area, ndataowneruid , nipecr):
        er = cls(
                    date=ndate,
                    reqstr_userid = nrqsteruid,
                    tp =  ThirdParty.objects.get(pk = ntpid),
                    data_store_system = ndatastore_system,
                    data_store_system_area = ndatastore_system_area,
                    # data_store =ndatastore,
                    data_owner_userid = ndataowneruid,
                    # data_store_export_claim =  nclaim,
                    ipecr = nipecr)
        return er
    

    class Meta:
        verbose_name = "EAB Request"
        verbose_name_plural = "EAB Requests"
        unique_together = [['tp', 'data_store_system','data_store_system_area' ]]


    def clean(self, *args, **kwargs):
        # check if there's a linked approval in an Approved state
        if(EAB_Approval.objects.filter(request__id=self.id).exists()):
            approval = EAB_Approval.objects.get(request__id=self.id)
            if(approval.decision == 'APP'):
                raise ValidationError('This EAB request is locked - ask an Export Control Manager to revoke the related EAB Approval first.')

        if(not validateUserName(self.reqstr_userid)):
            raise ValidationError('User name ' + self.reqstr_userid + ' appears invalid for field requestor user ID')

        if(not validateUserName(self.data_owner_userid)):
            raise ValidationError('User name ' + self.data_owner_userid + ' appears invalid for field Data owner user ID')

        super().clean(*args, **kwargs)


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        temp_str = self.reqstr_userid + ' req for ' + str(self.tp) + ' access to ' + str(self.data_store_system)
        temp_str += ' [' + str(self.data_store_system_area) + ']'
        return temp_str




## EAB Approval
class EAB_Approval(models.Model):
    request = models.ForeignKey(EAB_Request, on_delete=models.CASCADE, default = None)
    date = models.DateField('Date of Review')
    approver_userid = models.CharField('Approver User ID',max_length=10)
    decision =  models.CharField('Decision', max_length=3, choices = [ ('NYR','Not Yet Reviewed'),('APP','Approved'),('REJ','Rejected'),('PEN','Pending')])
    ecm_comment = models.CharField('ECM comment' , max_length=512) # Export Control Manager
    ipm_comment = models.CharField('IP Manager comment', max_length=512) # IP manager
    IT_comment = models.CharField('IT Comment', max_length=512) # IT comment


    @classmethod
    def create(cls, nreq, ndate, napprover, ndecision, necm_comment , nipm_comment, nIT_comment):
        aprv = cls(
                    request = EAB_Request.objects.get(pk = nreq),
                    date = ndate,
                    approver_userid = napprover,
                    decision =  ndecision,
                    ecm_comment = necm_comment,
                    ipm_comment = nipm_comment,
                    IT_comment =  nIT_comment
                    )
        return aprv


    class Meta:
        verbose_name = "EAB Approval"
        verbose_name_plural = "EAB Approvals"


    # debug setting flag here
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



    def __str__(self):
            return self.approver_userid + ' reviewed as ' + self.decision + ' on ' + str(self.date)

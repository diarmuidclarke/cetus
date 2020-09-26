from django.db import models


# A 3rd party, e.g. belcan UK
class ThirdParty(models.Model):
    legal_entity_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

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




# R=R Responsible Manager
class RRResponsibleManager(models.Model):
    firstname = models.CharField(max_length=50)
    familyname = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20)
    user_ac =  models.CharField('User account', max_length=10, default='<null>')
    
    class Meta:
        verbose_name = "R-R Responsible Manager"
        verbose_name_plural = "R-R Responsible Managers"

    def __str__(self):
            return self.firstname + ' @ R-R'


# what datastore is the requestor seeking to share
# implications for approvals, also useful for impact analysis
class EAB_DataStoreSystem(models.Model):
    DATASTORESYSTEM_CHOICES = [
        ('RRCS_INTEGRITY',  'Integrity'),
        ('RRCS_ARTISAN',    'Artisan'),
        ('RRCS_DOORS',      'Controls DOORS'),
        ('RRGAD_DOORS',     'R-R Winyard/Doxford DOORS'),
        ('RRCS_NAS',        'Controls Network Folder'),
        ('RRCS_CINCOM',     'CINCOM'),
        ('RRCS_TFS',        'TFS'),
        ('RRCS_OTHER',      'Other'),
    ]

    # to store the selection from the standard list of data store systems
    datastoresystem = models.CharField(
        'Data store system',
        max_length=20,
        choices=DATASTORESYSTEM_CHOICES,
        default='RRCS_OTHER',
    )

    # if datastoresystem is Other, then specify it in freetext here
    data_store_system_other_specify = models.CharField(max_length=256, default='todo')

    class Meta:
        verbose_name = "Data Store System"
        verbose_name_plural = "Data Store System"

    def __str__(self):
        if(str(self.datastoresystem) == 'RRCS_OTHER' and len(self.data_store_system_other_specify) > 0):
            return ('EAB Non standard data store : ' + self.data_store_system_other_specify)
        else:
            return (self.datastoresystem)





## EAB Request
class EAB_Request(models.Model):
    date = models.DateField('Date of Request')
    reqstr_userid = models.CharField('Requester User ID', max_length=10)
    tp = models.ForeignKey(ThirdParty,  related_name='third_party', on_delete=models.CASCADE)

    # e.g. integrity, artisan, nas drive
    data_store_system = models.ForeignKey( EAB_DataStoreSystem,  related_name='data_store_system', on_delete=models.CASCADE, null=True)  # todo : check this use of related_name

    # specify the part of the data store system being requested to share, e.g. a particular project in Artisan
    data_store = models.CharField( 'Date Store Area to be shared', max_length=256)

    # owner of that part of the data store system, e.g. owner of a specific network folder
    data_owner_userid =  models.CharField( 'Data Owner User ID', max_length=10)

    # export claim for this part of the data store
    data_store_export_claim = models.CharField('Export status of Data Store', max_length=512 )

    # ipecr - if known/needed
    ipecr = models.IntegerField('IPECR #')

    @classmethod
    def create(cls, ndate, nrqsteruid, ntpid, ndatastore, ndataowneruid , nclaim, nipecr):
        er = cls(
                    date=ndate,
                    reqstr_userid = nrqsteruid,
                    tp =  ThirdParty.objects.get(pk = ntpid),
                    data_store =ndatastore,
                    data_owner_userid = ndataowneruid,
                    data_store_export_claim =  nclaim,
                    ipecr = nipecr)
        return er
    
    class Meta:
        verbose_name = "EAB Request"
        verbose_name_plural = "EAB Requests"

    def __str__(self):
            return self.reqstr_userid + ' req for ' + str(self.tp) + ' access to ' + str(self.data_store_system) + ' [' + self.data_store + ']'





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

    def __str__(self):
            return self.approver_userid + ' reviewed as ' + self.decision + ' on ' + str(self.date)

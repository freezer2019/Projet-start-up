from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from autoslug.fields import AutoSlugField


class District(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	description = models.TextField(max_length=200, null=True, blank=True)
	date_ajout= models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('District')
		verbose_name_plural = _('Districts')
		ordering = ['date_ajout']

	def __str__(self):
		return self.nom

class Region(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	district = models.ForeignKey(District, on_delete = models.CASCADE, verbose_name="District")
	date_ajout = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Region')
		verbose_name_plural = _('Regions')
		ordering = ['date_ajout']

	def __str__(self):
		return self.nom

class Ville(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	region = models.ForeignKey(Region, on_delete = models.CASCADE, verbose_name="Region")
	date_ajout = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Ville')
		verbose_name_plural = _('Villes')
		ordering = ['date_ajout']

	def __str__(self):
		return self.nom + " de la région du " + self.region

class Secteur(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	ville = models.ForeignKey(Ville, on_delete = models.CASCADE, verbose_name="Ville")
	date_ajout = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Secteur')
		verbose_name_plural = _('Secteurs')
		ordering = ['date_ajout']

	def __str__(self):
		return self.nom + " de la ville " + self.ville

class Quartier(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	secteur = models.ForeignKey(Secteur, on_delete = models.CASCADE, verbose_name="Secteur")
	date_ajout = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Quartier')
		verbose_name_plural = _('Quartiers')
		ordering = ['date_ajout']

	def __str__(self):
		return self.nom + " du secteur " + self.secteur



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "Ministere"), (2, "Commissaire"), (3, "Policier"))
    user_type = models.CharField(default=3, choices=user_type_data, max_length=10)



class Ministere(models.Model):
    Sexe = (
        ('Masculin', 'M'),
        ('Feminin', 'F'),
    )
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    sexe = models.CharField(max_length=10, choices=Sexe, default='M', )
    date_de_naissance = models.DateTimeField(blank=False)
    lieu_de_naissance = models.OneToOneField(Ville, on_delete=models.CASCADE, blank=False)
    numero_cni = models.CharField(max_length=11, unique=True)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Le numéro entré n'est pas au bon format")
    telephone = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False)
    address = models.TextField()
    photo = models.ImageField(_('image'), blank=False, null=False, upload_to='Ministere')
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_actualisation = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Ministere')
        verbose_name_plural = _('Ministeres')
        ordering = ['date_ajout']

	def __str__(self):
		return '%s %s %s %s' % (self.first_name, self.last_name, self.email, self.telephone)


class Commissaire(models.Model):
    Sexe = (
        ('Masculin', 'M'),
        ('Feminin', 'F'),
    )
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=10, choices=Sexe, default='M', )
    date_de_naissance = models.DateTimeField(blank=False)
    lieu_de_naissance = models.OneToOneField(Ville, on_delete=models.CASCADE, blank=False)
    numero_cni = models.CharField(max_length=11, unique=True)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Le numéro entré n'est pas au bon format")
    telephone = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False)
    address = models.TextField()
    matricule = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(_('image'), blank=False, null=False, upload_to='Commissaire')
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_actualisation = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Commissaire')
        verbose_name_plural = _('Commissaires')
        ordering = ['date_ajout']

	def __str__(self):
		return '%s %s %s %s' % (self.first_name, self.last_name, self.email, self.telephone)


class Commissariat(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	ville = models.ForeignKey(Ville, on_delete = models.CASCADE, verbose_name="Ville")
	chef_du_commissariat =  models.OneToOneField(Commissaire, on_delete = models.CASCADE, verbose_name="Chef du Commissariat")
	date_ajout = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Commissariat')
		verbose_name_plural = _('Commissariats')
		ordering = ['date_ajout']



class Policier(models.Model):
	Sexe = (
		('Masculin', 'M'),
		('Feminin', 'F'),
	)
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	sexe = models.CharField(max_length=10, choices = Sexe, default='M',)
	date_de_naissance = models.DateTimeField(null=False, blank=False)
	lieu_de_naissance = models.OneToOneField(Ville, on_delete = models.CASCADE)
	numero_cni = models.CharField(max_length=11, unique=True)
	matricule = models.CharField(max_length=11, unique=True)
	mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Le numéro entré n'est pas au bon format")
	telephone = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False)
	address = models.TextField()
	photo = models.ImageField(_('image'), blank=False, null=False, upload_to='Policier')
	commissariat = models.ForeignKey(Commissariat, on_delete = models.CASCADE, verbose_name="Policier")
	date_ajout = models.DateTimeField(auto_now_add=True)
	date_actualisation = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name = _('Policier')
		verbose_name_plural = _('Policiers')
		ordering = ['date_ajout']

	def __str__(self):
		return '%s %s %s %s' % (self.first_name, self.last_name, self.email, self.telephone)

class Equipe_enquetrice(models.Model):
	nom = models.CharField(max_length=60, null=False, blank=False)
	commissaire_en_charge = models.ForeignKey(Commissaire, on_delete=models.CASCADE, verbose_name="Commissaire en charge de l'enquete")
	membres = models.ForeignKey(Policier, on_delete = models.CASCADE, verbose_name="Policiers enqueteurs")
	date_formation = models.DateTimeField(auto_now_add=True)



class Crime(models.Model):
	possibilites = (
		('Vol', 'Vol'),
		('Viol', 'Viol'),
		('Assassinat', 'Assassinat'),
		('Autres', 'Autres'),
	)
	nature = models.CharField(max_length=11, choices = possibilites, default='Vol',)
	description = models.TextField()
	secteur_de_commission = models.OneToOneField(Quartier, on_delete = models.CASCADE, verbose_name="Quartier de commssion du crime")
	equipe_enquetrice = models.OneToOneField(Equipe_enquetrice, on_delete = models.CASCADE, verbose_name="Equipe qui enquete sur le crime")
	resolu = models.BooleanField(_('crime résolu ?'), default=False)
	date_commission = models.DateTimeField(auto_now_add=True)
	date_actualisation = models.DateTimeField(auto_now=True)
	date_resolution = models.DateTimeField(auto_now=True)

def save(self, *args, **kwargs):
    if self.resolu and self.date_resolution is None:
        self.date_resolution = datetime.now()
    elif not self.resolu and self.date_resolution is not None:
        self.date_resolution = None
    super().save(*args, **kwargs)



class Delinquant(models.Model):
	Sexe = (
		('Masculin', 'M'),
		('Feminin', 'F'),
	)
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=60, null=False, blank=False)
	prenom = models.CharField(max_length=90, null=False, blank=False)
	sexe = models.CharField(max_length=10, choices = Sexe, default='M',)
	date_de_naissance = models.DateTimeField(null=False, blank=False)
	lieu_de_naissance = models.OneToOneField(Ville, on_delete = models.CASCADE)
	numero_cni = models.CharField(max_length=11, Blank=True)
	mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Le numéro entré n'est pas au bon format")
	telephone = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
	photo = models.ImageField(_('image'), blank=False, null=False, upload_to='Delinquant')
	crime = models.ForeignKey(Crime, on_delete = models.CASCADE, verbose_name="Crimes")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Ministere.objects.create(admin=instance)
        if instance.user_type == 2:
            Commissaire.objects.create(admin=instance)
        if instance.user_type == 3:
            Policier.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.Ministere.save()
    if instance.user_type == 2:
        instance.Commissaire.save()
    if instance.user_type == 3:
        instance.Policier.save()
    



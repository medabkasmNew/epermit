from django.db import models




class Role(models.TextChoices):
    OPERATOR = "operator", "Operator"
    TECHNICIEN = "technicien", "Technicien"
    FORMAN = "forman", "Forman"
    ENGINEER = "engineer", "Engineer"
    TEAM_LEADER = "team_leader", "Team leader"
    DEPARTEMENT_CHIEF = "departement_chief", "Departement chief"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"
class Department(models.TextChoices):
    WIRERODE = 'wirerode', 'Wirerode'
    QA = 'qa', 'QA'
    LOGISTICS = 'logistics', 'Logistics'
    HEAVY_MACHINE = 'heavy_machine', 'Heavy Machine'
    HSM = 'hsm', 'HSM'
    CRM = 'crm', 'CRM'
    HSPM = 'hspm', 'HSPM'
    SMP1 = 'smp1', 'SMP1'
    SMP2 = 'smp2', 'SMP2'
    SMP3 = 'smp3', 'SMP3'
    SMP4 = 'smp4', 'SMP4'
    RM1 = 'rm1', 'RM1'
    RM2 = 'rm2', 'RM2'
    RM3 = 'rm3', 'RM3'
    DRI1 = 'dri1', 'DRI1'
    DRI2 = 'dri2', 'DRI2'
    DRI3 = 'dri3', 'DRI3'
    PELLET1 = 'pellet1', 'Pellet1'
    PELLET2 = 'pellet2', 'Pellet2'
    IT = 'it', 'IT'
    HOLDING = 'holding', 'Holding'
    ADMINISTRATION = 'administration', 'Administration'
    ASU1 = 'asu1', 'ASU1'
    ASU2 = 'asu2', 'ASU2'
    ASU3 = 'asu3', 'ASU3'
    WTP1 = 'wtp1', 'WTP1'
    WTP2 = 'wtp2', 'WTP2'
    WTP3 = 'wtp3', 'WTP3'
    WTP4 = 'wtp4', 'WTP4'
    LIME1 = 'lime1', 'Lime1'
    LIME2 = 'lime2', 'Lime2'
    PIPE = 'pipe', 'Pipe'
    SHRIDER = 'shrider', 'Shrider'
    HARSCO = 'harsco', 'Harsco'
    TRANSPORTATION = 'transportation', 'Transportation'
    CEAW = 'ceaw', 'CEAW'
    GENERALE_SERVICES = 'general_services', 'General Services'
    INVESTEMENTS = 'investements', 'Investements'
    OTHER = 'other', 'Other'    
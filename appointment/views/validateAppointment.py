from appointment.models import *

"""
Check for conflicts between appointments given a doctor, a patient,
and the proposed time for the new appointment. This allows for edge
collisions, though. e.g. 14:00-14:30 and 14:30-15:00 is valid.
@param doctor The doctor to check the schedule for
@param patien The patient to check the schedule for
@param starttime The start time of the new appointment
@param endtime The end time of the new appointment
@param appointment (Optional) If the check should ignore that appointment (useful for updating).
@return True if the appointment is valid; False otherwise
"""
def isAppointmentValid( doctor, patient, date, starttime, endtime, appointment=None ):

    # Make sure the start time is before the end time
    # and that the appointment lasts at least 1 second.
    if starttime >= endtime:
        return False
    # Make sure the doctor doesn't have any conflicting appointments.
    for app in Appointment.objects.filter(a_doctor=doctor):
        # If the appointments are the same, then ignore it
        # since it means that it is the one that we are currently editing.
        if appointment != None and appointment == app:
            continue
        # If they're on different days, they don't overlap.
        if date != app.a_date:
            continue
        if app.a_starttime < endtime and app.a_endtime > starttime:
            return False
    # Make sure the patient doesn't have any conflicting appointments.
    for app in Appointment.objects.filter(a_patient=patient):
        # If the appointments are the same, then ignore it
        # since it means that it is the one that we are currently editing.
        if appointment != None and appointment == app:
            continue
        # If they're on different days, they don't overlap.
        if date != app.a_date:
            continue
        if app.a_starttime < endtime and app.a_endtime > starttime:
            return False

    return True

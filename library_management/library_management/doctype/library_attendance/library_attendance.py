# Copyright (c) 2023, Kabonge and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class LibraryAttendance(Document):
    def validate(self):
        if self.sign_in_time and self.sign_out_time:
            # If both sign-in and sign-out times are provided, set status to "Signed Out"
            self.status = "Signed Out"
        elif self.sign_in_time:
            # If only sign-in time is provided, set status to "Signed In"
            self.status = "Signed In"
        else:
            # If no sign-in or sign-out time is provided, set status to "Absent"
            self.status = "Absent"
            
        if self.status == "Sign In" and not self.is_valid_membership():
            frappe.throw("The member does not have a valid membership")

def is_valid_membership(self):
    # Check if a valid membership exists for the library member
    valid_membership = frappe.db.exists(
        "Library Membership",
        {
            "library_member": self.library_member,
            "docstatus": 1,
            "from_date": ("<=", self.sign_in_time),
            "to_date": (">=", self.sign_in_time),
            "is_paid": 1,  # Optional: You can check if the membership is paid
        },
    )

    return valid_membership is not None
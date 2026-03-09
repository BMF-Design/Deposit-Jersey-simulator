from engine.states import Role, GameState

SCENES = {

    # ---------- Tenant path ----------

    (Role.TENANT, GameState.START):
        "You are about to start a new tenancy. The landlord presents a tenancy agreement.",

    (Role.TENANT, GameState.AGREEMENT_SIGNED):
        "The agreement is signed. The landlord now asks for the deposit.",

    (Role.TENANT, GameState.DEPOSIT_PAID):
        "You have paid the deposit. The landlord must protect it in the official scheme.",

    (Role.TENANT, GameState.DEPOSIT_PROTECTED):
        "You receive confirmation that the landlord has protected the deposit in the scheme.",

    (Role.TENANT, GameState.MID_TENANCY):
        "The tenancy is underway. Small issues and responsibilities arise over time.",

    (Role.TENANT, GameState.END_NOTICE_GIVEN):
        "You decide to end the tenancy and must give proper notice to the landlord.",

    (Role.TENANT, GameState.CHECKOUT_DONE):
        "The tenancy ends and a checkout inspection compares the property to the original inventory.",

    (Role.TENANT, GameState.DEPOSIT_PROPOSED):
        "The landlord proposes deductions from the deposit for cleaning or damage.",

    (Role.TENANT, GameState.ADR_DISPUTE):
        "You may accept the deductions or raise a dispute through the deposit scheme's ADR service.",


    # ---------- Landlord path ----------

    (Role.LANDLORD, GameState.START):
        "A prospective tenant is ready to sign the tenancy agreement.",

    (Role.LANDLORD, GameState.AGREEMENT_SIGNED):
        "The agreement has been signed and the tenant pays the deposit.",

    (Role.LANDLORD, GameState.DEPOSIT_PAID):
        "You now hold the tenant's deposit. You must decide how to handle it.",

    (Role.LANDLORD, GameState.DEPOSIT_PROTECTED):
        "You must protect the tenant's deposit in the approved scheme within 30 days.",

    (Role.LANDLORD, GameState.MID_TENANCY):
        "The tenancy is progressing. Communication and maintenance matter.",

    (Role.LANDLORD, GameState.END_NOTICE_GIVEN):
        "The tenant gives notice to end the tenancy.",

    (Role.LANDLORD, GameState.CHECKOUT_DONE):
        "You inspect the property to assess its condition compared to the inventory.",

    (Role.LANDLORD, GameState.DEPOSIT_PROPOSED):
        "You decide whether deductions should be made from the tenant's deposit.",

    (Role.LANDLORD, GameState.ADR_DISPUTE):
        "The tenant disputes the deductions and the case may go to ADR adjudication.",
}
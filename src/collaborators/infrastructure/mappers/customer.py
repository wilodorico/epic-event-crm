from collaborators.domain.customer.customer import Customer
from collaborators.infrastructure.database.models.customer import CustomerModel


class CustomerMapper:
    @staticmethod
    def to_entity(model: CustomerModel) -> Customer:
        customer = Customer(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone_number=model.phone_number,
            company=model.company,
            commercial_contact_id=model.commercial_contact_id,
        )
        # Override the auto-generated timestamps with DB values
        customer.created_at = model.created_at
        customer.updated_at = model.updated_at
        return customer

    @staticmethod
    def to_model(entity: Customer) -> CustomerModel:
        model = CustomerModel(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone_number=entity.phone_number,
            company=entity.company,
            commercial_contact_id=entity.commercial_contact_id,
        )
        # Set timestamps manually if they exist
        if entity.created_at:
            model.created_at = entity.created_at
        if entity.updated_at:
            model.updated_at = entity.updated_at
        return model

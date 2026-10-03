from pydantic import BaseModel, field_validator


class PredictorRequest(BaseModel):
    email_type: str
    country: str
    city: str

    @field_validator("email_type", "country", "city")
    @classmethod
    def validate_text_input(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Input values must not be empty")
        return value
    



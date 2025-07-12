from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, TelField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class CheckoutForm(FlaskForm):
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired()])
    
    # Shipping Address
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    address2 = StringField('Address 2 (Optional)', validators=[Optional(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('ZIP/Postal Code', validators=[DataRequired(), Length(min=3, max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    
    # Payment Information
    payment_method = SelectField('Payment Method', 
                               choices=[
                                   ('credit', 'Credit/Debit Card'),
                                   ('paypal', 'PayPal')
                               ],
                               validators=[DataRequired()])
    
    # Credit Card Fields (conditionally shown)
    card_number = StringField('Card Number', 
                            validators=[Optional(), 
                                      Length(min=13, max=19, message='Card number must be between 13-19 digits')])
    card_expiry = StringField('Expiry Date (MM/YY)', 
                             validators=[Optional(), 
                                       Length(min=4, max=5, message='Please use MM/YY format')])
    card_cvv = StringField('CVV', 
                          validators=[Optional(), 
                                    Length(min=3, max=4, message='CVV must be 3-4 digits')])
    card_name = StringField('Name on Card', 
                           validators=[Optional(), 
                                     Length(min=2, max=100)])
    
    # Submit Button
    submit = SubmitField('Place Order')
    
    def validate(self, **kwargs):
        # First validate the basic fields
        if not super().validate():
            return False
            
        # If payment method is credit card, validate card fields
        if self.payment_method.data == 'credit':
            card_fields = [
                (self.card_number, 'Card number is required'),
                (self.card_expiry, 'Expiry date is required'),
                (self.card_cvv, 'CVV is required'),
                (self.card_name, 'Name on card is required')
            ]
            
            for field, error_msg in card_fields:
                if not field.data or not str(field.data).strip():
                    field.errors.append(error_msg)
                    return False
                    
            # Additional validation for card number (basic Luhn check)
            try:
                digits = [int(d) for d in str(self.card_number.data) if d.isdigit()]
                if len(digits) < 13 or len(digits) > 19:
                    self.card_number.errors.append('Invalid card number length')
                    return False
                    
                # Luhn algorithm check
                checksum = 0
                digits.reverse()
                for i, d in enumerate(digits):
                    if i % 2 == 1:
                        d *= 2
                        if d > 9:
                            d -= 9
                    checksum += d
                
                if checksum % 10 != 0:
                    self.card_number.errors.append('Invalid card number')
                    return False
                    
            except (ValueError, IndexError):
                self.card_number.errors.append('Invalid card number format')
                return False
                
        return True

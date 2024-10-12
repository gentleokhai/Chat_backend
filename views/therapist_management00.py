from flask import Blueprint, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import User
from models.therapist_model import Therapist
from decorators.super_user import superuser_required

therapist_blueprint = Blueprint('therapist', __name__)


class CreateTherapistResource(Resource):
    """Handles creating a new therapist profile."""

    def post(self):
        """Create a therapist profile.
        ---
        tags:
          - Therapists
        parameters:
          - in: body
            name: body
            required: true
            description: Therapist profile to create
            schema:
              type: object
              properties:
                first_name:
                  type: string
                  example: "John"
                last_name:
                  type: string
                  example: "Doe"
                specialty:
                  type: string
                  example: "Psychology"
                fees:
                  type: string
                  example: "$100"
                rmdc_ref_no:
                  type: string
                  example: "12345"
                qualification:
                  type: string
                  example: "PhD in Psychology"
                availability:
                  type: array
                  items:
                    type: string
                    example: "available"
        responses:
          201:
            description: Therapist created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Therapist profile created successfully"
        """
        data = request.get_json()
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()

        if not current_user:
            return {"error": "User not found"}, 404

        therapist = Therapist(
            user_id=current_user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialty=data.get('specialty'),
            fees=data.get('fees'),
            rmdc_ref_no=data.get('rmdc_ref_no'),
            qualification=data.get('qualification'),
            availability=data.get('availability'),
            created_by=current_user,
            updated_by=current_user
        )
        therapist.save()
        return {"message": "Therapist profile created successfully"}, 201


class ReadTherapistResource(Resource):
    """Handles retrieving a therapist's profile."""

    def get(self, therapist_id):
        """Get details of a therapist by ID.
        ---
        tags:
          - Therapists
        parameters:
          - in: path
            name: therapist_id
            required: true
            type: string
            description: The ID of the therapist to retrieve
        responses:
          200:
            description: Therapist details
            schema:
              type: object
              properties:
                first_name:
                  type: string
                  example: "John"
                last_name:
                  type: string
                  example: "Doe"
                specialty:
                  type: string
                  example: "Psychology"
                fees:
                  type: string
                  example: "$100"
                rmdc_ref_no:
                  type: string
                  example: "12345"
                qualification:
                  type: string
                  example: "PhD in Psychology"
                availability:
                  type: array
                  items:
                    type: string
                    example: "available"
        """
        therapist = Therapist.objects(id=therapist_id).first()
        if not therapist:
            return {"error": "Therapist not found"}, 404

        return {
            "first_name": therapist.first_name,
            "last_name": therapist.last_name,
            "specialty": therapist.specialty,
            "fees": therapist.fees,
            "rmdc_ref_no": therapist.rmdc_ref_no,
            "qualification": therapist.qualification,
            "availability": therapist.availability,
            "created_by": str(therapist.created_by.id),
            "updated_by": str(therapist.updated_by.id)
        }, 200


class ListTherapistsResource(Resource):
    """Handles listing all therapists."""

    def get(self):
        """Get a list of all therapists.
        ---
        tags:
          - Therapists
        responses:
          200:
            description: A list of therapists
            schema:
              type: array
              items:
                type: object
                properties:
                  first_name:
                    type: string
                    example: "John"
                  last_name:
                    type: string
                    example: "Doe"
        """
        therapists = Therapist.objects()
        return [
            {
                "first_name": t.first_name,
                "last_name": t.last_name,
                "specialty": t.specialty,
                "fees": t.fees,
                "created_by": str(t.created_by.id),
                "updated_by": str(t.updated_by.id)
            } for t in therapists
        ], 200


class DeleteTherapistResource(Resource):
    """Handles deleting a therapist."""

    @superuser_required
    def delete(self, therapist_id):
        """Delete a therapist profile.
        ---
        tags:
          - Therapists
        parameters:
          - in: path
            name: therapist_id
            required: true
            type: string
            description: The ID of the therapist to delete
        responses:
          200:
            description: Therapist deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Therapist deleted successfully"
          404:
            description: Therapist not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Therapist not found"
        """
        therapist = Therapist.objects(id=therapist_id).first()
        if not therapist:
            return {"error": "Therapist not found"}, 404

        therapist.delete()
        return {"message": "Therapist deleted successfully"}, 200


class UpdateAcceptanceStatus(Resource):
    """Handles updating the acceptance status of a therapist."""

    @superuser_required
    def put(self, therapist_id):
        """Update the acceptance status of a therapist.
        ---
        tags:
          - Therapists
        parameters:
          - in: path
            name: therapist_id
            required: true
            type: string
            description: The ID of the therapist
          - in: body
            name: body
            required: true
            description: Acceptance status to update
            schema:
              type: object
              properties:
                acceptance_status:
                  type: string
                  example: "accepted"
        responses:
          200:
            description: Acceptance status updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Acceptance status updated successfully"
          404:
            description: Therapist not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Therapist not found"
        """
        data = request.get_json()
        acceptance_status = data.get('acceptance_status')

        therapist = Therapist.objects(id=therapist_id).first()
        if not therapist:
            return {"error": "Therapist not found"}, 404

        therapist.acceptance_status = acceptance_status
        therapist.updated_by = User.objects(id=get_jwt_identity()).first()
        therapist.save()

        return {"message": "Acceptance status updated successfully"}, 200


# Register the Resources
therapist_blueprint.add_url_rule(
    '/api/v1/therapists/create-therapist',
    view_func=CreateTherapistResource.as_view('create_therapist')
)
therapist_blueprint.add_url_rule(
    '/api/v1/therapists/view-single-therapist/<string:therapist_id>',
    view_func=ReadTherapistResource.as_view('read_therapist')
)
therapist_blueprint.add_url_rule(
    '/api/v1/therapists/view-all-therapist',
    view_func=ListTherapistsResource.as_view('view_all_therapists')
)
therapist_blueprint.add_url_rule(
    '/api/v1/therapists/delete-therapist/<string:therapist_id>',
    view_func=DeleteTherapistResource.as_view('delete_therapist')
)
therapist_blueprint.add_url_rule(
    '/api/v1/therapists/update-therapist-status/<string:therapist_id>',
    view_func=UpdateAcceptanceStatus.as_view('update_acceptance_status')
)

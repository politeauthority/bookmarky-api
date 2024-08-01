"""
    Bookmarky Api
    Controller Model
    Base

"""
import json
import logging

from flask import make_response, request, jsonify

from bookmarky.shared.utils import xlate


def get_model(model, entity_id: int = None) -> dict:
    """Base GET operation for a model.
    :unit-test: TestCtrlModelsBase::test__get_model
    @todo: This is just stupidy written.
    @todo: Throw an error if we return multiple results
    @todo: Gate based on user's access to records that only belong to them
    """
    entity = model()

    data = {
        "status": "error",
        "message": "",
        "object": {},
        "object_type": entity.model_name
    }
    request_args = request.args
    query = {}
    if "query" in request_args:
        query = xlate.url_decode_json_flask(request_args["query"])
        if query:
            logging.crticial("Expecting to run a query, but that has not been built yet.")
            return make_response(jsonify(data), 501)
    else:
        search_type = _determine_entity_search_type(entity, entity_id, request_args)
        if search_type == "cant":
            data["message"] = "Missing required search ctriteria."
            return make_response(jsonify(data), 400)

        # Get the entity by it's ID
        elif search_type == "by-id":
            logging.debug(f"Getting {entity.model_name} by ID.")
            entity_found = entity.get_by_id(entity_id)
            not_found_msg = f"{entity.model_name.title()} not found by id {entity_id}"

        # Get the entity by it's UX field
        elif search_type == "by-ux-field":
            entity_found = get_entity_by_ux_field(entity, request_args)
            not_found_msg = f"{entity.model_name.title()} not found by ux field"

        # Get the entity by it's UX key
        elif search_type == "by-ux-key":
            entity_found = get_entity_by_ux_keys(entity, request_args)
            not_found_msg = f"{entity.model_name.title()} not found by ux key"

        # Get the entity by it's fields.
        elif search_type == "by-fields":
            entity_found = get_entity_by_fields(entity, request_args)
            not_found_msg = f"{entity.model_name.title()} not found by fields"

        if not entity_found:
            data["message"] = not_found_msg
            return make_response(jsonify(data), 404)

    data["status"] = "success"
    data["object"] = entity.json()
    return data


def post_model(model, entity_id: int = None, generated_data: dict = {}):
    """Base POST operation for a model. Create or modify a entity.
    To edit an entity it's strongly encouraged you pass the entity ID in the URL. Otherwise we rely
    on database keys.
    If a model is immutabel then we can skip looking for the entity in the database.
    If a model is not createable, an model MUST be found in the database.
    @param entity_id: The ID of the entity. Used when UPDATING and entity.
    @param generated_data: This is used in instances like ApiKey generation, where fields are
        determined server side.
    """
    data = {
        "status": "error"
    }
    entity = model()
    entity_found = False
    if not entity.immutable:
        if entity_id:
            try:
                entity_id = xlate.convert_any_to_int(entity_id)
            except AttributeError:
                data["status"] = "Error"
                data["message"] = "Entity ID must be int"
                return make_response(jsonify(data), 400)
            if not entity.get_by_id(entity_id):
                data["status"] = "Error"
                data["message"] = "Could not find %s ID: %s" % (entity.model_name, entity_id)
                return make_response(jsonify(data), 404)
            else:
                entity_found = True
                logging.info("POST - Found entity by ID: %s" % entity)

    # Dont allow api creates on api uncreateble models
    if not entity.id and not entity.createable:
        data["message"] = "Not allowed to create entity %s" % entity.model_name
        logging.warning("Attempting to create an ID ")
        return make_response(jsonify(data), 400)

    # If we cant decode a JSON payload return an error.
    try:
        request_args = request.get_json()
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"Recieved data that cant be decoded to JSON: {e}")
        return make_response("ERROR", 401)

    search_type = _determine_entity_search_type(entity, entity_id, request_args)
    
    if search_type == "cant":
        entity_found = False

    # Get the entity by it's ID if we dont find it by ID and we're given one this is an error.
    elif search_type == "by-id":
        logging.debug(f"Getting {entity.model_name} by ID.")
        entity_found = entity.get_by_id(entity_id)
        not_found_msg = f"{entity.model_name.title()} not found by id {entity_id}"
        return make_response(jsonify(data), 404)

    # Get the entity by it's UX field
    elif search_type == "by-ux-field":
        entity_found = get_entity_by_ux_field(entity, request_args)
        not_found_msg = f"{entity.model_name.title()} not found by ux field"
        logging.warning(not_found_msg)

    # Get the entity by it's UX key
    elif search_type == "by-ux-key":
        entity_found = get_entity_by_ux_keys(entity, request_args)
        not_found_msg = f"{entity.model_name.title()} not found by ux key"
        logging.warning(not_found_msg)

    # If there's server side generated data, override the request data with that info.
    if generated_data:
        request_args.update(generated_data)

    if not entity_found:
        logging.warning(
            "Entity was not found, attempting to create a new entity of type: {entity.model_name}"
        )

    # logging.info("\nREQUEST:\n%s\n%s" % (request.url, request_data))
    entity = _post_update_entity(entity, request_args, generated_data)
    entity.save()
    data["status"] = "success"
    data["object"] = entity.json()
    data["object_type"] = entity.model_name
    return data, 201


def delete_model(model, entity_id: int = None):
    """Base DELETE a model."""
    entity = model()
    data = {
        "status": "Success",
        "object_type": entity.model_name
    }
    entity_found = False
    if entity_id:
        # Get the entity by it's ID
        logging.debug(f"Getting {entity.model_name} by ID.")
        entity_found = entity.get_by_id(entity_id)
        not_found_msg = f"{entity.model_name.title()} not found by id {entity_id}"

    else:
        # If we cant decode a JSON payload return an error.
        try:
            request_args = request.get_json()
        except json.decoder.JSONDecodeError as e:
            logging.warning(f"Recieved data that cant be decoded to JSON: {e}")
            return make_response("ERROR", 401)

        search_type = _determine_entity_search_type(entity, entity_id, request_args)

        if search_type == "cant":
            data["message"] = "Missing required search ctriteria."
            logging.warning(data["message"])
            return make_response(jsonify(data), 400)

        # Get the entity by it's UX field
        elif search_type == "by-ux-field":
            entity_found = get_entity_by_ux_field(entity, request_args)
            not_found_msg = f"{entity.model_name.title()} not found by ux field"

        # Get the entity by it's UX key
        elif search_type == "by-ux-key":
            entity_found = get_entity_by_ux_keys(entity, request_args)
            not_found_msg = f"{entity.model_name.title()} not found by ux key"

        if not entity_found:
            data["message"] = not_found_msg
            logging.warning(data["message"])
            return make_response(jsonify(data), 404)

    entity.delete()
    data["message"] = "%s deleted successfully" % entity.model_name
    data["object"] = entity.json()
    return make_response(jsonify(data), 202)


def get_entity_by_ux_field(entity, request_args: dict):
    for field_name, field_info in entity.field_map.items():
        if "extra" in field_info and field_info["extra"] == "UNIQUE":
            if field_info["name"] in request_args:
                ux_field = field_info["name"]
                ux_value = request_args[ux_field]
                break
    logging.debug("Attempting to get {entity.model_name} by ux field: {ux_field} value: {value}")
    return entity.get_by_field(ux_field, ux_value)


def get_entity_by_ux_keys(entity, request_args: dict):
    """Finds a model based on it's unique keys based on data coming from the request.
    :unit-test:
    """
    if not hasattr(entity, "ux_key") or not entity.ux_key:
        logging.warning("Entity %s has no ux keys set, cant search by ux key")
        return False
    fields = {}
    for key in entity.ux_key:
        if key not in request_args:
            logging.warning("Field: %s is not a ux key for %s" % (key, entity))
            continue
        fields[key] = request_args[key]
    logging.debug(f"Getting entity by fields: {fields}")
    return entity.get_by_ux_key(**fields)


def get_entity_by_fields(entity, request_args: dict):
    """Finds an entity based on request fields sent along with the request.
    :unit-test:
    """
    search_fields = []
    for r_arg_key, r_arg_value in request_args.items():
        if r_arg_key not in entity.field_map:
            continue
        for field_name, field in entity.field_map.items():
            if field["name"] != r_arg_key:
                continue
        if "api_searchable" not in entity.field_map[r_arg_key]:
            continue
        search_field = {
            "field": r_arg_key,
            "value": r_arg_value,
            "op": "eq"
        }
        search_fields.append(search_field)
    return entity.get_by_fields(search_fields)


def _post_update_entity(entity, request_data, generated_data):
    # Check through the fields and see if they should be applied to the entity.
    for field_name, field_value in request_data.items():
        update_field = False
        for entity_field_name, entity_field in entity.field_map.items():
            # if entity_field_name == "value":
            #     import ipdb; ipdb.set_trace()
            if entity_field["name"] == field_name:
                if "api_writeable" not in entity_field and field_name not in generated_data:
                    logging.warning("Entity %s can not write field %s via an API request" % (
                        entity,
                        field_name))
                    continue
                else:
                    update_field = True
                # if entity_field_name == "value":
                #     import ipdb; ipdb.set_trace()
        if update_field:
            logging.info("Entity: %s updating field: %s value: %s" % (
                entity,
                field_name,
                field_value))
            setattr(entity, field_name, field_value)
    return entity


def _determine_entity_search_type(entity, entity_id=None, request_args: dict = None) -> str:
    """Figure out how we search for a single model entity based on the request data sent in, and
    the model's makeup.
    I actually really am enjoying this method. however it needs to be simplified and tested.
    @todo: everything I said above.
    """
    logging.debug(request_args)
    if entity_id:
        return "by-id"

    # Check for UX keys within the model and the request
    if entity.ux_key:
        has_all_ux_key_fields = True
        for ux_key in entity.ux_key:
            if ux_key not in request_args:
                has_all_ux_key_fields = False
                break
        if has_all_ux_key_fields:
            return "by-ux-key"

    # Check for a unique field we can seearch on
    for field_name, field_info in entity.field_map.items():
        if "extra" in field_info and field_info["extra"] == "UNIQUE":
            if field_name in request_args:
                return "by-ux-field"

    by_fields = True
    for request_arg in request_args:
        if request_arg not in entity.field_map:
            by_fields = False
    if by_fields:
        return "by-fields"

    return "cant"


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_base.py

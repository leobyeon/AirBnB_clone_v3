#!/usr/bin/python3
""" Place Amenities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def all_amenity_places(place_id, amenity_id=None):
    """ retrieves, deletes or adds amenities in a place """

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    try:
        flip = True
        amenity_list = place.amenity_ids
    except AttributeError:
        flip = False
        amenity_list = [x.id for x in place.amenities]

    if request.method == 'GET':
        return (jsonify([x.to_dict() for x in place.amenities]))

    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        if amenity.id not in amenity_list:
            abort(404)
        if flip is False:
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity_id)
        place.save()
        return (jsonify({}), 200)

    if request.method == 'POST':
        if amenity.id in amenity_list:
            return (jsonify(amenity.to_dict()), 200)
        if flip is True:
            place.amenity_ids.append(amenity_id)
        else:
            place.amenities.append(amenity)
        place.save()
        return (jsonify(amenity.to_dict()), 201)

from flask import Flask, request, jsonify
from models import AdRepository

app = Flask(__name__)

repository = AdRepository()

@app.route('/ads', methods=['GET'])
def get_all_ads():
	ads = repository.get_all()
	return jsonify([ad.to_dict() for ad in ads]), 200

@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
	ad = repository.get_by_id(ad_id)

	if ad is None:
		return jsonify({ 'error': 'Объявление не найдено' }), 404
	return jsonify(ad.to_dict()), 200

@app.route('/ads', methods=['POST'])
def create_ad():
	data = request.get_json()

	if not data:
		return jsonify({ 'error': 'Запрос должен быть в формате JSON' }), 400

	title = data.get('title')
	description = data.get('description')
	owner = data.get('owner')

	if not title or not description or not owner:
		return jsonify({ 'error': 'Поля title, description, owner должны быть заполнены' }), 400

	new_ad = repository.create(
		title=title,
		description=description,
		owner=owner
	)

	return jsonify(new_ad.to_dict()), 201

@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
	ad = repository.get_by_id(ad_id)

	if ad is None:
		return jsonify({ 'error': 'Объявление не найдено' }), 404

	data = request.get_json()

	if not data:
		return jsonify({ 'error': 'Запрос должен быть в формате JSON' }), 400

	updated_ad = repository.update(
		ad_id=ad_id,
		title=data.get('title'),
		description=data.get('description'),
		owner=data.get('owner')
	)
	return jsonify(updated_ad.to_dict()), 200

@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
	ad = repository.get_by_id(ad_id)

	if ad is None:
		return jsonify({ 'error': 'Объявление не найдено' }), 404

	success = repository.delete(ad_id)

	if success:
		return jsonify({ 'message': f'Объявление {ad_id} успешно удалено' }), 200
	else:
		return jsonify({ 'error': 'Не удалось удалить объявление' }), 500

@app.errorhandler(404)
def not_found(error):
	return jsonify({ 'error': 'Маршрут не найден' }), 404
@app.errorhandler(405)
def method_not_allowed(error):
	return jsonify({'error': 'Метод не разрешён для этого маршрута'}), 405
@app.errorhandler(500)
def internal_error(error):
	return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
	print("GET/ads          - получить все объявления")
	print("GET/ads/<id>     - получить объявление по ID")
	print("POST/ads         - создать объявление")
	print("PUT/ads/<id>     - обновить объявление")
	print("DELETE /ads/<id> - удалить объявление")
	app.run(debug=True, host='0.0.0.0', port=5000)
import os
from flask import Flask, request, jsonify, render_template
from personalization_module import initialize_data, get_personalized_feed

app = Flask(__name__)


NEWS_DATA, USER_PROFILES = initialize_data()


USER_PROFILES_FOR_TEMPLATE = USER_PROFILES 


@app.route('/')
def index():
 
    return render_template(
        'index.html', 
        user_ids=list(USER_PROFILES.keys()), 
        user_profiles=USER_PROFILES_FOR_TEMPLATE 
    )


@app.route('/api/feed', methods=['POST'])
def generate_feed():
    data = request.json
    
    user_id = data.get('user_id')
    is_breaking = data.get('is_breaking', False)
    
    if not user_id or user_id not in USER_PROFILES:
        return jsonify({"error": "Geçersiz Kullanıcı ID."}), 404

    try:
        final_feed = get_personalized_feed(
            user_id, 
            is_breaking, 
            NEWS_DATA, 
            USER_PROFILES
        )
        
        response = {
            "user_id": user_id,
            "priority_override": is_breaking,
            "feed_count": len(final_feed),
            "feed": final_feed,
            "user_interest": USER_PROFILES[user_id]['interests']
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Akış oluşturma sırasında hata oluştu: {str(e)}"}), 500


if __name__ == '__main__':
    # Flask'ın her çalıştığında index'e erişebilmesi için gerekli (Jinja2 hatası önleme)
    from personalization_module import USER_PROFILES
    app.run(debug=True)

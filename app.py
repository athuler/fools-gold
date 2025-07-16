from flask import Flask, render_template, jsonify
import json
import os
import time
import threading
import logging
from dotenv import load_dotenv
from social_fetcher import SocialMediaFetcher

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging for both development and production
if __name__ != '__main__':
    # Running under gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.clear()  # Clear any existing handlers
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.propagate = False  # Prevent propagation to avoid duplicates
    
    # Also configure the root logger to use gunicorn's handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()  # Clear any existing handlers
    root_logger.handlers = gunicorn_logger.handlers
    root_logger.setLevel(gunicorn_logger.level)
    
else:
    # Running in development mode
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

# Configuration
DATA_FILE = os.environ.get('DATA_FILE', 'engagement_data.json')
REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 4 * 60 * 60))  # Default 4 hours in seconds

# Video and player mappings
VIDEOS = {
    'kings': 'Kings',
    'car_wash': 'Car Wash', 
    'glue': 'Glue',
    'cracks': 'Cracks',
    'dimension_20': 'Dimension 20',
    'puppy_bowl': 'Puppy Bowl',
    'breast_milk': 'Breast Milk',
    'hair': 'Hair',
    'holes': 'Holes',
    'brennan': 'Brennan'
}

PLAYER_VIDEOS = {
    'Trapp': ['glue', 'cracks', ('puppy_bowl', 0.5), ('holes', 0.5), ('brennan', 1/3)],
    'Jordan': ['kings', 'hair', ('car_wash', 0.5), 'breast_milk', ('brennan', 1/3)],
    'Rekha': ['dimension_20', ('car_wash', 0.5), ('puppy_bowl', 0.5), ('holes', 0.5), ('brennan', 1/3)]
}

# Social media URLs
SOCIAL_URLS = {
    'kings': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMGy2goOQSR',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMGy8RuNDqI/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527078952171523341',
        'youtube': 'https://www.youtube.com/shorts/UjHk90dxX20',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789089874490818560/no-kings-in-this-country-except-a-few-of-the'
    },
    'car_wash': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG0NabtH7O',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG0OcPpSQO/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527082014449716494',
        'youtube': 'https://www.youtube.com/shorts/HD5pyGbO_Is',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789090638794801152/whos-your-favorite-sexy-dropout-car-wash-team'
    },
    'glue': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG0j6qCAjE',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG0jk2tbeR/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527082801120677133',
        'youtube': 'https://www.youtube.com/shorts/gMpx4A2lRTE',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789090765137690624/youve-never-seen-anything-as-satisfying-as'
    },
    'cracks': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG1A9LKqlQ',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG1BIPM41Z/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527083827689229582',
        'youtube': 'https://www.youtube.com/shorts/1lnl0jYln8s',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789091008304578560/if-you-love-hearing-oddly-satisfying-cracks-at-the'
    },
    'dimension_20': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG1HnRz9CN',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMGzkMNNMXg/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527080453610704183',
        'youtube': 'https://www.youtube.com/shorts/5feqZBLXrMg',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789090265340280832/presenting-the-brand-new-season-dimension-20'
    },
    'puppy_bowl': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG1eOyqxs2',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG1d62Mhmf/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527084871580142861',
        'youtube': 'https://www.youtube.com/shorts/aagwlycxv_k',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789091260709355520/forget-having-to-choose-between-the-big-game-and'
    },
    'breast_milk': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG10FKBp3C',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG11avO8qa/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527085610322890039',
        'youtube': 'https://www.youtube.com/shorts/nfwmaVlp_hY',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789091518113792000/can-jordan-correctly-identify-three-of-their'
    },
    'hair': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG2C-6PSo4',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG2ELMvZdg/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527086113614318862',
        'youtube': 'https://www.youtube.com/shorts/wQVIfuNIc9I',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789091640471076864/now-everywhere-erika-goes-a-roast-of-sam-reich'
    },
    'holes': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG2RwdtsH3',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG2SXRMojo/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527086642415422734',
        'youtube': 'https://www.youtube.com/shorts/Wm8SMsmWCts',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789091767963336704/the-lady-said-3000-worth-of-animated-buttholes'
    },
    'brennan': {
        'threads': 'https://www.threads.com/@gamechangershow/post/DMG22Q7B_IV',
        'instagram': 'https://www.instagram.com/gamechangershow/reel/DMG24Zjyg1j/',
        'tiktok': 'https://www.tiktok.com/@gamechangershow/video/7527087942339267895',
        'youtube': 'https://www.youtube.com/shorts/oO4kgmYivoQ',
        'tumblr': 'https://www.tumblr.com/gamechangershow/789092023188733952/brennans-announcement'
    }
}

class DataManager:
    def __init__(self):
        self.data = {}
        self.last_update = 0
        self.lock = threading.Lock()
        self.fetcher = SocialMediaFetcher()
        
    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    self.data = json.load(f)
                    app.logger.info(f"Loaded data from {DATA_FILE}")
            else:
                self.data = {video: [] for video in VIDEOS.keys()}
                app.logger.info("Initialized empty data structure")
        except Exception as e:
            app.logger.error(f"Error loading data: {e}")
            self.data = {video: [] for video in VIDEOS.keys()}
    
    def save_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
            app.logger.info(f"Saved data to {DATA_FILE}")
        except Exception as e:
            app.logger.error(f"Error saving data: {e}")
    
    def should_refresh(self):
        if not self.data:
            return True
        
        # Check if any video has data points
        for video_data in self.data.values():
            if video_data:
                latest_timestamp = max(point['timestamp'] for point in video_data)
                if time.time() - latest_timestamp > REFRESH_INTERVAL:
                    return True
        
        return len([v for v in self.data.values() if v]) == 0
    
    def fetch_social_data(self, platform, url):
        return self.fetcher.fetch_data(platform, url)
    
    def refresh_data(self):
        with self.lock:
            if not self.should_refresh():
                return
            
            app.logger.info("Starting data refresh...")
            timestamp = int(time.time())
            
            for video_id, platforms in SOCIAL_URLS.items():
                total_views = 0
                total_likes = 0
                total_comments = 0
                platform_data = {}
                
                for platform, url in platforms.items():
                    try:
                        data = self.fetch_social_data(platform, url)
                        total_views += data['views']
                        total_likes += data['likes']
                        total_comments += data['comments']
                        
                        platform_data[f'views_{platform}'] = data['views']
                        platform_data[f'likes_{platform}'] = data['likes']
                        platform_data[f'comments_{platform}'] = data['comments']
                        
                        app.logger.info(f"Fetched {platform} data for {video_id}")
                    except Exception as e:
                        app.logger.error(f"Error fetching {platform} data for {video_id}: {e}")
                
                entry = {
                    'timestamp': timestamp,
                    'total_views': total_views,
                    'total_likes': total_likes,
                    'total_comments': total_comments,
                    **platform_data
                }
                
                if video_id not in self.data:
                    self.data[video_id] = []
                self.data[video_id].append(entry)
            
            self.save_data()
            app.logger.info("Data refresh completed")

data_manager = DataManager()

def get_latest_video_scores():
    # Reload data from file to get latest updates
    data_manager.load_data()
    
    scores = {}
    for video_id, video_data in data_manager.data.items():
        if video_data:
            latest = video_data[-1]
            scores[video_id] = {
                'name': VIDEOS[video_id],
                'combined': latest['total_views'] + latest['total_likes'] + latest['total_comments'],
                'views': latest['total_views'],
                'likes': latest['total_likes'],
                'comments': latest['total_comments'],
                # Platform-specific data for frontend recalculation
                'views_youtube': latest.get('views_youtube', 0),
                'likes_youtube': latest.get('likes_youtube', 0),
                'comments_youtube': latest.get('comments_youtube', 0),
                'views_tiktok': latest.get('views_tiktok', 0),
                'likes_tiktok': latest.get('likes_tiktok', 0),
                'comments_tiktok': latest.get('comments_tiktok', 0),
                'views_tumblr': latest.get('views_tumblr', 0),
                'likes_tumblr': latest.get('likes_tumblr', 0),
                'comments_tumblr': latest.get('comments_tumblr', 0),
                'views_instagram': latest.get('views_instagram', 0),
                'likes_instagram': latest.get('likes_instagram', 0),
                'comments_instagram': latest.get('comments_instagram', 0),
                'views_threads': latest.get('views_threads', 0),
                'likes_threads': latest.get('likes_threads', 0),
                'comments_threads': latest.get('comments_threads', 0)
            }
    return scores

def get_player_scores():
    video_scores = get_latest_video_scores()
    player_scores = {}
    
    for player, videos in PLAYER_VIDEOS.items():
        combined = views = likes = comments = 0
        
        for video_spec in videos:
            if isinstance(video_spec, tuple):
                video_id, weight = video_spec
            else:
                video_id, weight = video_spec, 1.0
            
            if video_id in video_scores:
                video_score = video_scores[video_id]
                combined += video_score['combined'] * weight
                views += video_score['views'] * weight
                likes += video_score['likes'] * weight
                comments += video_score['comments'] * weight
        
        player_scores[player] = {
            'name': player,
            'combined': int(combined),
            'views': int(views),
            'likes': int(likes),
            'comments': int(comments)
        }
    
    return player_scores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/videos')
def api_videos():
    return jsonify(get_latest_video_scores())

@app.route('/api/players')
def api_players():
    return jsonify(get_player_scores())

@app.route('/api/trends')
def api_trends():
    # Reload data from file to get latest updates
    data_manager.load_data()
    
    trends = {'videos': {}, 'players': {}}
    
    # Video trends
    for video_id, video_data in data_manager.data.items():
        if video_data:
            trends['videos'][video_id] = {
                'name': VIDEOS[video_id],
                'data': [{
                    'timestamp': point['timestamp'],
                    'combined': point['total_views'] + point['total_likes'] + point['total_comments'],
                    'views': point['total_views'],
                    'likes': point['total_likes'],
                    'comments': point['total_comments'],
                    # Platform-specific data for frontend recalculation
                    'views_youtube': point.get('views_youtube', 0),
                    'likes_youtube': point.get('likes_youtube', 0),
                    'comments_youtube': point.get('comments_youtube', 0),
                    'views_tiktok': point.get('views_tiktok', 0),
                    'likes_tiktok': point.get('likes_tiktok', 0),
                    'comments_tiktok': point.get('comments_tiktok', 0),
                    'views_tumblr': point.get('views_tumblr', 0),
                    'likes_tumblr': point.get('likes_tumblr', 0),
                    'comments_tumblr': point.get('comments_tumblr', 0),
                    'views_instagram': point.get('views_instagram', 0),
                    'likes_instagram': point.get('likes_instagram', 0),
                    'comments_instagram': point.get('comments_instagram', 0),
                    'views_threads': point.get('views_threads', 0),
                    'likes_threads': point.get('likes_threads', 0),
                    'comments_threads': point.get('comments_threads', 0)
                } for point in video_data]
            }
    
    # Player trends
    for player in PLAYER_VIDEOS.keys():
        player_data = []
        
        # Get all timestamps
        all_timestamps = set()
        for video_data in data_manager.data.values():
            all_timestamps.update(point['timestamp'] for point in video_data)
        
        for timestamp in sorted(all_timestamps):
            combined = views = likes = comments = 0
            
            for video_spec in PLAYER_VIDEOS[player]:
                if isinstance(video_spec, tuple):
                    video_id, weight = video_spec
                else:
                    video_id, weight = video_spec, 1.0
                
                # Find data point for this timestamp
                video_data = data_manager.data.get(video_id, [])
                point = next((p for p in video_data if p['timestamp'] == timestamp), None)
                
                if point:
                    combined += (point['total_views'] + point['total_likes'] + point['total_comments']) * weight
                    views += point['total_views'] * weight
                    likes += point['total_likes'] * weight
                    comments += point['total_comments'] * weight
            
            player_data.append({
                'timestamp': timestamp,
                'combined': int(combined),
                'views': int(views),
                'likes': int(likes),
                'comments': int(comments)
            })
        
        trends['players'][player] = {
            'name': player,
            'data': player_data
        }
    
    return jsonify(trends)

data_manager = DataManager()
_initialized = False

def initialize_app():
    """Initialize the application with data loading and background refresh"""
    global _initialized
    if _initialized:
        app.logger.info("App already initialized, skipping...")
        return
    
    _initialized = True
    app.logger.info("Starting app initialization...")
    app.logger.info("Loading data...")
    data_manager.load_data()

    app.logger.info(f"Data refresh every {REFRESH_INTERVAL} seconds")

    # Start background refresh
    def background_refresh():
        while True:
            if data_manager.should_refresh():
                app.logger.info("Data is stale, starting refresh...")
                data_manager.refresh_data()
            else:
                app.logger.info("Data is fresh, skipping refresh.")
            
            # Check every minute if we need to refresh
            app.logger.info("Sleeping for 60 seconds before next check...")
            time.sleep(60)

    refresh_thread = threading.Thread(target=background_refresh, daemon=True)
    refresh_thread.start()

    app.logger.info("App initialization complete. Data refresh running in background.")

with app.app_context():
    if __name__ != '__main__':
        # Running under gunicorn
        initialize_app()

if __name__ == '__main__':
    initialize_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
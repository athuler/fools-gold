# Fool's Gold

Tracking the scores for Game Changer's [*Fool's Gold*](https://www.dropout.tv/videos/fool-s-gold).

In Game Changer's episode "Fool's Gold" (Season 7, Episode 8, released July 14, 2025), 10 videos were posted across various social media platforms.

## Video Scoring

Each video sums their number of views, likes, and comments it received across all social media platforms. Users are able to toggle between a combined score (view + likes + comments), total views, total likes, or total comments.

|        | Threads | Instagram | TikTok | YT Shorts |
| ---- | --- | --- | --- | --- |
| Kings | [Link](https://www.threads.com/@gamechangershow/post/DMGy2goOQSR) | [Link](https://www.instagram.com/gamechangershow/reel/DMGy8RuNDqI/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527078952171523341) | [Link](https://www.youtube.com/shorts/UjHk90dxX20) |
| Car Wash | [Link](https://www.threads.com/@gamechangershow/post/DMG0NabtH7O) | [Link](https://www.instagram.com/gamechangershow/reel/DMG0OcPpSQO/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527082014449716494) | [Link](https://www.youtube.com/shorts/HD5pyGbO_Is) |
| Glue | [Link](https://www.threads.com/@gamechangershow/post/DMG0j6qCAjE) | [Link](https://www.instagram.com/gamechangershow/reel/DMG0jk2tbeR/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527082801120677133) | [Link](https://www.youtube.com/shorts/gMpx4A2lRTE) |
| Cracks | [Link](https://www.threads.com/@gamechangershow/post/DMG1A9LKqlQ) | [Link](https://www.instagram.com/gamechangershow/reel/DMG1BIPM41Z/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527083827689229582) | [Link](https://www.youtube.com/shorts/1lnl0jYln8s) |
| Dimension 20 | [Link](https://www.threads.com/@gamechangershow/post/DMG1HnRz9CN) | [Link](https://www.instagram.com/gamechangershow/reel/DMGzkMNNMXg/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527080453610704183) | [Link](https://www.youtube.com/shorts/5feqZBLXrMg) |
| Puppy Bowl | [Link](https://www.threads.com/@gamechangershow/post/DMG1eOyqxs2) | [Link](https://www.instagram.com/gamechangershow/reel/DMG1d62Mhmf/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527084871580142861) | [Link](https://www.youtube.com/shorts/aagwlycxv_k) |
| Breast Milk | [Link](https://www.threads.com/@gamechangershow/post/DMG10FKBp3C) | [Link](https://www.instagram.com/gamechangershow/reel/DMG11avO8qa/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527085610322890039) | [Link](https://www.youtube.com/shorts/nfwmaVlp_hY) |
| Hair | [Link](https://www.threads.com/@gamechangershow/post/DMG2C-6PSo4) | [Link](https://www.instagram.com/gamechangershow/reel/DMG2ELMvZdg/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527086113614318862) | [Link](https://www.youtube.com/shorts/wQVIfuNIc9I) |
| Holes | [Link](https://www.threads.com/@gamechangershow/post/DMG2RwdtsH3) | [Link](https://www.instagram.com/gamechangershow/reel/DMG2SXRMojo/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527086642415422734) | [Link](https://www.youtube.com/shorts/Wm8SMsmWCts) |
| Brennan | [Link](https://www.threads.com/@gamechangershow/post/DMG22Q7B_IV) | [Link](https://www.instagram.com/gamechangershow/reel/DMG24Zjyg1j/) | [Link](https://www.tiktok.com/@gamechangershow/video/7527087942339267895) | [Link](https://www.youtube.com/shorts/oO4kgmYivoQ) |

> [!NOTE]
> We are purposefully not scoring Twitter engagement

## Player Scoring

- **Trapp**: Glue, Cracks, 0.5 * Puppy Bowl, 0.5 * Holes, 1/3 * Brennan
- **Jordan**: Kings, Hair, 0.5 * Car Wash, Breast Milk, 1/3 * Brennan
- **Rekha**: Dimension 20, 0.5 * Car Wash, 0.5 * Puppy Bowl, 0.5 * Holes, 1/3 * Brennan

## Page Layout

This is a one page website with the following sections:

1. **Video Ranking**
    Displays the ranking of all videos with a toggle to toggle between modes (combined, total views, ...)
2. **Player Ranking**
    Displays the ranking of all players with a toggle to toggle between modes (combined, total views, ...)
3. **Historical Trends**
    Display using two linegraphs how the scores of the videos and players have changed since July 15th, 2025.

## Tech Stack

- Frontend: ?
- Backend: Python
- Infrastructure: Google Cloud Run
- Data Storage: Google Cloud Storage

## Data Storage

The engagement data are saved as a single JSON file in the following format:

```json
{
    "kings":[
        {
            "timestamp":123456,
            "total_views": 123,
            "total_likes": 123,
            "total_comments": 123,
            "views_threads": 123,
            "likes_threads": 123,
            "comments_threads": 123,
            "views_instagram": 123,
            ...
        },
        {"timestamp":1234212, ...}
    ],
    "car_wash": ...,
    ...
}
```

When loading the page, if it has been more than 4 hours since the last data point, new social data are fetched for each video and social platform and added to the JSON file. Otherwise, the latest social data from the JSON file is used.
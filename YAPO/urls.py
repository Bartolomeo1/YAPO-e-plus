"""YAPO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import json
from datetime import datetime

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

import videos.aux_functions
import videos.const
from videos import views

# from django.contrib import admin
# admin.autodiscover()

# actor_alias_list = ActorAliasViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
#
# actor_alias_detail = ActorAliasViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# actor_list = ActorViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# actor_detail = ActorViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actor-alias', views.ActorAliasViewSet)
router.register(r'actor', views.ActorViewSet)
router.register(r'actor-tag', views.ActorTagViewSet)
router.register(r'scene', views.SceneViewSet)
router.register(r'scene-tag', views.SceneTagViewSet)
router.register(r'website', views.WebsiteViewSet)
router.register(r'folder', views.FolderViewSet)
router.register(r'folder-local', views.LocalSceneFoldersViewSet)
router.register(r'playlist', views.PlaylistViewSet)
# router.register(r'^upload/(?P<filename>[^/]+)', views.FileUploadView.as_view())


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^videos/', include('videos.urls')),
                  url(r'^api/', include(router.urls)),
                  url(r'^$', views.angualr_index, name='angular-index'),
                  url(r'^upload/', views.AssetAdd.as_view()),
                  url(r'^scrape-actor/', views.ScrapeActor.as_view()),
                  url(r'^play-scene/', views.play_in_vlc),
                  url(r'^open-folder/', views.OpenFolder.as_view()),
                  url(r'^add-items/', views.AddItems.as_view()),
                  url(r'^settings/', views.settings),
                  url(r'^ffmpeg/', views.ffmpeg),
                  url(r'^tag-multiple-items/', views.tag_multiple_items),
                  url(r'^play/', views.display_video)
                  # url(r'^admin/', admin.site.urls, name='admin')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])

#  Startup script checks settings.json and creates it if it doesn't exist
setting_version = videos.const.SETTINGS_VERSION
current_setting_version = 0

default_dict = { 'settings_version': setting_version, 'vlc_path': "", 'last_all_scene_tag': "" }
need_update = False

try:
    f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'r')
    x = f.read()

    if x == "":
        need_update = True
        f.close()
        print("Setting.json is empty")
        f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'w')
        f.write(json.dumps(default_dict))
        f.close()

    else:
        # print(x)

        settings_content = json.loads(x)
        f.close()

        if ('settings_version' not in settings_content) or (
                int(settings_content['settings_version']) < setting_version):

            current_setting_version = int(settings_content['settings_version'])
            if current_setting_version < 2:
                need_update = True
                for x in settings_content:
                    if x in default_dict:
                        default_dict[x] = settings_content[x]

                # default_dict['settings_version'] = SETTINGS_VERSION

                f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'w')
                f.write(json.dumps(default_dict))
                f.close()

                f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'r')
                x = f.read()
                settings_content = json.loads(x)

        print("VLC location: " + settings_content['vlc_path'])
        videos.const.VLC_PATH = settings_content['vlc_path']
        if settings_content['last_all_scene_tag'] != "":
            # 2016-08-14 18:03:10.153443
            videos.const.LAST_ALL_SCENE_TAG = datetime.strptime(settings_content['last_all_scene_tag'],
                                                                "%Y-%m-%d %H:%M:%S")
            print("The last full scene tagging was done {}\n".format(videos.const.LAST_ALL_SCENE_TAG))

    f.close()

except FileNotFoundError:
    f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'w')
    f.close()

    f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'w')
    f.write(json.dumps(default_dict))
    f.close()

if need_update:
    if videos.aux_functions.actor_folder_from_name_to_id():
        f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'r')
        x = f.read()
        settings_content = json.loads(x)
        f.close()
        settings_content['settings_version'] = setting_version

        f = open(os.path.abspath(os.path.join(BASE_DIR, 'settings.json')), 'w')
        f.write(json.dumps(settings_content))
        f.close()

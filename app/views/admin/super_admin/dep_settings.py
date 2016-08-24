from flask import request
from flask_admin import expose
from super_admin_base import SuperAdminBaseView, SETTINGS

from app.settings import get_settings, set_settings
from app.helpers.data_getter import DataGetter
from app.helpers.data import save_to_db
from werkzeug.datastructures import ImmutableMultiDict
from app.views.admin.models_views.events import EventsView
from app.models.image_config import ImageConfig
from app.models.image_sizes import ImageSizes

class SuperAdminSettingsView(SuperAdminBaseView):
    PANEL_NAME = SETTINGS

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        if request.method == 'POST':
            if 'event-thumbnail_width' in request.form:
                im_size = DataGetter.get_image_sizes()
                if im_size and im_size[0].type:
                    for im in im_size:
                        im_type = im.type
                        im.full_width = request.form[im_type + '-large_width']
                        im.full_height = request.form[im_type + '-large_height']
                        im.full_aspect = request.form.get(im_type + '-large_aspect', 'off')
                        im.icon_width = request.form[im_type + '-icon_width']
                        im.icon_height = request.form[im_type + '-icon_height']
                        im.icon_aspect = request.form.get(im_type + '-icon_aspect', 'off')
                        im.thumbnail_width = request.form[im_type + '-thumbnail_width']
                        im.thumbnail_height = request.form[im_type + '-thumbnail_height']
                        im.thumbnail_aspect = request.form.get(im_type + '-thumbnail_aspect', 'off')
                        im.logo_width = request.form['logo_width']
                        im.logo_height = request.form['logo_height']
                        save_to_db(im, "Image Sizes saved")
                else:
                    print request.form['profile-large_width']
                    im_size = ImageSizes(type='profile',
                                         full_width=request.form['profile-large_width'],
                                         full_height=request.form['profile-large_width'],
                                         full_aspect=request.form.get('profile-large_aspect', 'off'),
                                         icon_width=request.form['profile-icon_width'],
                                         icon_height=request.form['profile-icon_width'],
                                         icon_aspect=request.form.get('profile-icon_aspect', 'off'),
                                         thumbnail_width=request.form['profile-thumbnail_width'],
                                         thumbnail_height=request.form['profile-thumbnail_width'],
                                         thumbnail_aspect=request.form.get('profile-thumbnail_aspect', 'off'),
                                         logo_width=None,
                                         logo_height=None)
                    save_to_db(im_size, "Image Sizes saved")
                    im_size = ImageSizes(type='event',
                                         full_width=request.form['event-large_width'],
                                         full_height=request.form['event-large_height'],
                                         full_aspect=request.form.get('event-large_aspect', 'off'),
                                         icon_width=request.form['event-icon_width'],
                                         icon_height=request.form['event-icon_height'],
                                         icon_aspect=request.form.get('event-icon_aspect', 'off'),
                                         thumbnail_width=request.form['event-thumbnail_width'],
                                         thumbnail_height=request.form['event-thumbnail_height'],
                                         thumbnail_aspect=request.form.get('event-thumbnail_aspect', 'off'),
                                         logo_width=request.form['logo_width'],
                                         logo_height=request.form['logo_height'])
                    save_to_db(im_size, "Image Sizes saved")
                im_config = DataGetter.get_image_configs()
                if im_config:
                    for config in im_config:
                        config.size = request.form.get('size_' + config.page, '')
                        save_to_db(config, "Image Config Saved")
                else:
                    config = ImageConfig(page='front',
                                         size=request.form['size_front'])
                    save_to_db(config, "Image Config Saved")
                    config = ImageConfig(page='mysession',
                                         size=request.form['size_mysession'])
                    save_to_db(config, "Image Config Saved")
                    config = ImageConfig(page='event',
                                         size=request.form['size_event'])
                    save_to_db(config, "Image Config Saved")
                    config = ImageConfig(page='speaker_event',
                                         size=request.form.get('size_speaker_event', ''))
                    save_to_db(config, "Image Config Saved")
                    config = ImageConfig(page='speaker_dashboard',
                                         size=request.form.get('size_speaker_dashboard', ''))
                    save_to_db(config, "Image Config Saved")

            if 'service_fee' in request.form:
                dic = ImmutableMultiDict(request.form)
            else:
                dic = dict(request.form.copy())
                for i in dic:
                    v = dic[i][0]
                    if not v:
                        dic[i] = None
                    else:
                        dic[i] = v
            set_settings(**dic)

        settings = get_settings()
        fees = DataGetter.get_fee_settings()
        event_view = EventsView()
        image_config = DataGetter.get_image_configs()
        image_sizes = DataGetter.get_image_sizes()

        return self.render(
            '/gentelella/admin/super_admin/settings/settings.html',
            settings=settings,
            fees=fees,
            payment_currencies=DataGetter.get_payment_currencies(),
            included_settings=event_view.get_module_settings(),
            image_config=image_config,
            image_sizes=image_sizes
        )

    # @expose('/update', methods=('POST'))
    # def update_view(self):
    #     print request.form
    #     # set_settings(request.form[])

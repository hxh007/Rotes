# coding=utf-8

DEFAULT_SUPPER_USER = [
    {
    'username': 'admin',
    'fullname': u'管理员',
    'mobile': '13455556666',
    'password': 'a1s2d3f4',
    'management': 'ADMIN'
    }
]
DEFAULT_SUPPER_MANAGEMENT = [
    {
        'name': 'ADMIN',
        'alias': u'超级管理员'
    }

]
DEFAULT_ACTION = [
    {
        "codename": "GET",
        "alias": u"查看"
    },
    {
        "codename": "POST",
        "alias": u"添加"
    },
    {
        "codename": "PUT",
        "alias": u"修改"
    },
    {
        "codename": "DELETE",
        "alias": u"删除"
    }
]
DEFAULT_ROLES = [
    {
        "name": "one",
        "alias": u"一线"
    },
    {
        "name": "LEVEL2",
        "alias": u"二线值班"
    },
    {
        "name": "LEVEL2.5",
        "alias": u"2.5线"
    },
    {
        "name": "LEVEL3",
        "alias": u"三线值班"
    },
    {
        "name": "LEVEL4",
        "alias": u"四线值班"
    },
]
DEFAULT_TEMPTEXT = [
    {
        'name': u'短信模板',
        'content': u'记得明天9:00值班'
    }
]
# 部门
DEFAULT_DEPARTMENT = [
    {
        'name':"MODULE_OP",
        'alias': u'系统运维部'
    },

    {
        'name': 'MODULE_SEC',
        'alias': u'网络安全部'
    },
    {
        'name': 'MODULE_PLDEV',
        'alias': u'平台开发部'
    },
    {
        'name': 'MODULE_VSOURCE',
        'alias': u'视频技术中心信源技术部'
    },
    {
        'name': 'MODULE_VAPP',
        'alias': u'视频技术中心应用开发部'
    },
    {
        'name': 'MODULE_VDATA',
        'alias': u'视频技术中心数据技术部'
    },
    {
        'name': 'MODULE_APP',
        'alias': u'应用开发部'
    },
    {
        'name': 'MODULE_IDC',
        'alias': u'基础设施部'
    },
    {
        'name': 'MODULE_MUTUAL',
        'alias': u'新媒体创新孵化中心\互动融合中心'
    },
    {
        'name': 'MODULE_IPTV',
        'alias': u'IP电视事业部'
    },
    {
        'name': 'MODULE_CCP',
        'alias': u'共产党员网'
    },
    {
        'name': 'MODULE_MD',
        'alias': u'移动开发中心'
    },
    {
        'name': 'MODULE_IT',
        'alias': u'IT支持组'
    },
    {
        'name': 'MODULE_UD',
        'alias': u'用户数据中心'

    }
    ]
# 权限
DEFAULT_PERMISSIONS = [
    {
        'department': 'MODULE_OP',
        'codename': 'GET',
        'alias': u'系统运维部值班表：查询'
    },
    {
        'department': 'MODULE_OP',
        'codename': 'POST',
        'alias': u'系统运维部值班表：创建'
    },
    {
        'department': 'MODULE_OP',
        'codename': 'PUT',
        'alias': u'系统运维部值班表：修改'
    },
    {
        'department': 'MODULE_OP',
        'codename': 'DELETE',
        'alias': u'系统运维部值班表：删除'
    },
    {
        'department': 'MODULE_SEC',
        'codename': 'GET',
        'alias': u'网络安全部值班表：查询'
    },
    {
        'department': 'MODULE_SEC',
        'codename': 'POST',
        'alias': u'网络安全部值班表：创建'
    },
    {
        'department': 'MODULE_SEC',
        'codename': 'PUT',
        'alias': u'网络安全部值班表：修改'
    },
    {
        'department': 'MODULE_SEC',
        'codename': 'DELETE',
        'alias': u'网络安全部值班表：删除'
    },
    {
        'department': 'MODULE_PLDEV',
        'codename': 'GET',
        'alias': u'平台开发部值班表：查询'
    },
    {
        'department': 'MODULE_PLDEV',
        'codename': 'POST',
        'alias': u'平台开发部值班表：创建'
    },
    {
        'department': 'MODULE_PLDEV',
        'codename': 'PUT',
        'alias': u'平台开发部值班表：修改'
    },
    {
        'department': 'MODULE_PLDEV',
        'codename': 'DELETE',
        'alias': u'平台开发部值班表：删除'
    },
    {
        'department': 'MODULE_VSOURCE',
        'codename': 'GET',
        'alias': u'视频技术中心信源技术部值班表：查询'
    },
    {
        'department': 'MODULE_VSOURCE',
        'codename': 'POST',
        'alias': u'视频技术中心信源技术部值班表：创建'
    },
    {
        'department': 'MODULE_VSOURCE',
        'codename': 'PUT',
        'alias': u'视频技术中心信源技术部值班表：修改'
    },
    {
        'department': 'MODULE_VSOURCE',
        'codename': 'DELETE',
        'alias': u'视频技术中心信源技术部值班表：删除'
    },
    {
        'department': 'MODULE_VAPP',
        'codename': 'GET',
        'alias': u'视频技术中心应用开发部值班表：查询'
    },
    {
        'department': 'MODULE_VAPP',
        'codename': 'POST',
        'alias': u'视频技术中心应用开发部值班表：创建'
    },
    {
        'department': 'MODULE_VAPP',
        'codename': 'PUT',
        'alias': u'视频技术中心应用开发部值班表：修改'
    },
    {
        'department': 'MODULE_VAPP',
        'codename': 'DELETE',
        'alias': u'视频技术中心应用开发部值班表：删除'
    },
    {
        'department': 'MODULE_VDATA',
        'codename': 'GET',
        'alias': u'视频技术中心数据技术部值班表：查询'
    },
    {
        'department': 'MODULE_VDATA',
        'codename': 'POST',
        'alias': u'视频技术中心数据技术部值班表：创建'
    },
    {
        'department': 'MODULE_VDATA',
        'codename': 'PUT',
        'alias': u'视频技术中心数据技术部值班表：修改'
    },
    {
        'department': 'MODULE_VDATA',
        'codename': 'DELETE',
        'alias': u'视频技术中心数据技术部值班表：删除'
    },
    {
        'department': 'MODULE_APP',
        'codename': 'GET',
        'alias': u'应用开发部排班表：查询'
    },
    {
        'department': 'MODULE_APP',
        'codename': 'POST',
        'alias': u'应用开发部排班表：创建'
    },
    {
        'department': 'MODULE_APP',
        'codename': 'PUT',
        'alias': u'应用开发部排班表：修改'
    },
    {
        'department': 'MODULE_APP',
        'codename': 'DELETE',
        'alias': u'应用开发部排班表：删除'
    },
    {
        'department': 'MODULE_IDC',
        'codename': 'GET',
        'alias': u'基础设施部排班表：查询'
    },
    {
        'department': 'MODULE_IDC',
        'codename': 'POST',
        'alias': u'基础设施部排班表：创建'
    },
    {
        'department': 'MODULE_IDC',
        'codename': 'PUT',
        'alias': u'基础设施部排班表：修改'
    },
    {
        'department': 'MODULE_IDC',
        'codename': 'DELETE',
        'alias': u'基础设施部排班表：删除'
    },
    {
        'department': 'MODULE_MUTUAL',
        'codename': 'GET',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：查询'
    },
    {
        'department': 'MODULE_MUTUAL',
        'codename': 'POST',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：创建'
    },
    {
        'department': 'MODULE_MUTUAL',
        'codename': 'PUT',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：修改'
    },
    {
        'department': 'MODULE_MUTUAL',
        'codename': 'DELETE',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：删除'
    },
    {
        'department': 'MODULE_IPTV',
        'codename': 'GET',
        'alias': u'IP电视事业部排班表：查询'
    },
    {
        'department': 'MODULE_IPTV',
        'codename': 'POST',
        'alias': u'IP电视事业部排班表：创建'
    },
    {
        'department': 'MODULE_IPTV',
        'codename': 'PUT',
        'alias': u'IP电视事业部排班表：修改'
    },
    {
        'department': 'MODULE_IPTV',
        'codename': 'DELETE',
        'alias': u'IP电视事业部排班表：删除'
    },
    {
        'department': 'MODULE_CCP',
        'codename': 'GET',
        'alias': u'共产党员网排班表：查询'
    },
    {
        'department': 'MODULE_CCP',
        'codename': 'POST',
        'alias': u'共产党员网排班表：创建'
    },
    {
        'department': 'MODULE_CCP',
        'codename': 'PUT',
        'alias': u'共产党员网排班表：修改'
    },
    {
        'department': 'MODULE_CCP',
        'codename': 'DELETE',
        'alias': u'共产党员网排班表：删除'
    },
    {
        'department': 'MODULE_MD',
        'codename': 'GET',
        'alias': u'移动开发中心排班表：查询'
    },
    {
        'department': 'MODULE_MD',
        'codename': 'POST',
        'alias': u'移动开发中心排班表：创建'
    },
    {
        'department': 'MODULE_MD',
        'codename': 'PUT',
        'alias': u'移动开发中心排班表：修改'
    },
    {
        'department': 'MODULE_MD',
        'codename': 'DELETE',
        'alias': u'移动开发中心排班表：删除'
    },
    {
        'department': 'MODULE_IT',
        'codename': 'GET',
        'alias': u'IT支持组排班表：查询'
    },
    {
        'department': 'MODULE_IT',
        'codename': 'POST',
        'alias': u'IT支持组排班表：创建'
    },
    {
        'department': 'MODULE_IT',
        'codename': 'PUT',
        'alias': u'IT支持组排班表：修改'
    },
    {
        'department': 'MODULE_IT',
        'codename': 'DELETE',
        'alias': u'IT支持组排班表：删除'
    },
    {
        'department': 'MODULE_UD',
        'codename': 'GET',
        'alias': u'用户数据中心排班表：查询'

    },
    {
        'department': 'MODULE_UD',
        'codename': 'POST',
        'alias': u'用户数据中心排班表：创建'

    },
    {
        'department': 'MODULE_UD',
        'codename': 'PUT',
        'alias': u'用户数据中心排班表：修改'

    },
    {
        'department': 'MODULE_UD',
        'codename': 'DELETE',
        'alias': u'用户数据中心排班表：删除'

    }
]

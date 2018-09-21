# coding=utf-8
# 超级管理员
DEFAULT_SUPPER_USER = [
    {
    'username': 'admin',
    'fullname': u'超级管理员',
    'mobile': '13455556666',
    'password': 'a1s2d3f4',
    'management': 'S_MANAGEMENT'
    }
]
# 管理组
DEFAULT_SUPPER_MANAGEMENT = [
    {
        'name': 'S_MANAGEMENT',
        'alias': u'超级管理'
    },
    {
        'name': 'BU_MANAGEMENT',
        'alias': u'业务管理'
    },
    {
        'name': 'TF_MANAGEMENT',
        'alias': u'三、四线部门管理'
    },
    {
        'name':"OP_MANAGEMENT",
        'alias': u'系统运维部管理'
    },

    {
        'name': 'SEC_MANAGEMENT',
        'alias': u'网络安全部管理'
    },
    {
        'name': 'PLDEV_MANAGEMENT',
        'alias': u'平台开发部管理'
    },
    {
        'name': 'VSOURCE_MANAGEMENT',
        'alias': u'视频技术中心信源技术部管理'
    },
    {
        'name': 'VAPP_MANAGEMENT',
        'alias': u'视频技术中心应用开发部管理'
    },
    {
        'name': 'VDATA_MANAGEMENT',
        'alias': u'视频技术中心数据技术部管理'
    },
    {
        'name': 'APP_MANAGEMENT',
        'alias': u'应用开发部管理'
    },
    {
        'name': 'IDC_MANAGEMENT',
        'alias': u'基础设施部管理'
    },
    {
        'name': 'MUTUAL_MANAGEMENT',
        'alias': u'新媒体创新孵化中心\互动融合中心管理'
    },
    {
        'name': 'IPTV_MANAGEMENT',
        'alias': u'IP电视事业部管理'
    },
    {
        'name': 'CCP_MANAGEMENT',
        'alias': u'共产党员网管理'
    },
    {
        'name': 'MD_MANAGEMENT',
        'alias': u'移动开发中心管理'
    },
    {
        'name': 'IT_MANAGEMENT',
        'alias': u'IT支持组管理'
    },
    {
        'name': 'UD_MANAGEMENT',
        'alias': u'用户数据中心管理'

    }
]
# 操作类型
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
# 角色
DEFAULT_ROLES = [
    {
        "name": "LEVEL1",
        "alias": u"一线值班"
    },
    {
        "name": "LEVEL2",
        "alias": u"二线值班"
    },
    {
        "name": "LEVEL2.5",
        "alias": u"2.5线值班"
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
        'name': 'SMS',
        'content': u'央视网大运维提醒您：您大运维值班时间是明天({TOMORROW})9:00至次日9:00，在岗时间为9:00至21:00，请务必准时到岗。谢谢~'
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

    },
    {
        'name': 'MODULE_VT',
        'alias': u'三、四线部门'

    }
    ]
# 权限
DEFAULT_PERMISSIONS = [
    {
        'department': 'MODULE_OP',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'系统运维部值班表：查询'
    },
    {
        'department': 'MODULE_OP',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'系统运维部值班表：创建'
    },
    {
        'department': 'MODULE_OP',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'系统运维部值班表：修改'
    },
    {
        'department': 'MODULE_OP',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'系统运维部值班表：删除'
    },
    {
        'department': 'MODULE_SEC',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'网络安全部值班表：查询'
    },
    {
        'department': 'MODULE_SEC',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'网络安全部值班表：创建'
    },
    {
        'department': 'MODULE_SEC',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'网络安全部值班表：修改'
    },
    {
        'department': 'MODULE_SEC',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'网络安全部值班表：删除'
    },
    {
        'department': 'MODULE_PLDEV',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'平台开发部值班表：查询'
    },
    {
        'department': 'MODULE_PLDEV',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'平台开发部值班表：创建'
    },
    {
        'department': 'MODULE_PLDEV',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'平台开发部值班表：修改'
    },
    {
        'department': 'MODULE_PLDEV',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'平台开发部值班表：删除'
    },
    {
        'department': 'MODULE_VSOURCE',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'视频技术中心信源技术部值班表：查询'
    },
    {
        'department': 'MODULE_VSOURCE',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'视频技术中心信源技术部值班表：创建'
    },
    {
        'department': 'MODULE_VSOURCE',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'视频技术中心信源技术部值班表：修改'
    },
    {
        'department': 'MODULE_VSOURCE',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'视频技术中心信源技术部值班表：删除'
    },
    {
        'department': 'MODULE_VAPP',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'视频技术中心应用开发部值班表：查询'
    },
    {
        'department': 'MODULE_VAPP',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'视频技术中心应用开发部值班表：创建'
    },
    {
        'department': 'MODULE_VAPP',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'视频技术中心应用开发部值班表：修改'
    },
    {
        'department': 'MODULE_VAPP',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'视频技术中心应用开发部值班表：删除'
    },
    {
        'department': 'MODULE_VDATA',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'视频技术中心数据技术部值班表：查询'
    },
    {
        'department': 'MODULE_VDATA',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'视频技术中心数据技术部值班表：创建'
    },
    {
        'department': 'MODULE_VDATA',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'视频技术中心数据技术部值班表：修改'
    },
    {
        'department': 'MODULE_VDATA',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'视频技术中心数据技术部值班表：删除'
    },
    {
        'department': 'MODULE_APP',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'应用开发部排班表：查询'
    },
    {
        'department': 'MODULE_APP',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'应用开发部排班表：创建'
    },
    {
        'department': 'MODULE_APP',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'应用开发部排班表：修改'
    },
    {
        'department': 'MODULE_APP',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'应用开发部排班表：删除'
    },
    {
        'department': 'MODULE_IDC',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'基础设施部排班表：查询'
    },
    {
        'department': 'MODULE_IDC',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'基础设施部排班表：创建'
    },
    {
        'department': 'MODULE_IDC',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'基础设施部排班表：修改'
    },
    {
        'department': 'MODULE_IDC',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'基础设施部排班表：删除'
    },
    {
        'department': 'MODULE_MUTUAL',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：查询'
    },
    {
        'department': 'MODULE_MUTUAL',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：创建'
    },
    {
        'department': 'MODULE_MUTUAL',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：修改'
    },
    {
        'department': 'MODULE_MUTUAL',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'新媒体创新孵化中心\互动融合中心排班表：删除'
    },
    {
        'department': 'MODULE_IPTV',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'IP电视事业部排班表：查询'
    },
    {
        'department': 'MODULE_IPTV',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'IP电视事业部排班表：创建'
    },
    {
        'department': 'MODULE_IPTV',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'IP电视事业部排班表：修改'
    },
    {
        'department': 'MODULE_IPTV',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'IP电视事业部排班表：删除'
    },
    {
        'department': 'MODULE_CCP',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'共产党员网排班表：查询'
    },
    {
        'department': 'MODULE_CCP',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'共产党员网排班表：创建'
    },
    {
        'department': 'MODULE_CCP',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'共产党员网排班表：修改'
    },
    {
        'department': 'MODULE_CCP',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'共产党员网排班表：删除'
    },
    {
        'department': 'MODULE_MD',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'移动开发中心排班表：查询'
    },
    {
        'department': 'MODULE_MD',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'移动开发中心排班表：创建'
    },
    {
        'department': 'MODULE_MD',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'移动开发中心排班表：修改'
    },
    {
        'department': 'MODULE_MD',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'移动开发中心排班表：删除'
    },
    {
        'department': 'MODULE_IT',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'IT支持组排班表：查询'
    },
    {
        'department': 'MODULE_IT',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'IT支持组排班表：创建'
    },
    {
        'department': 'MODULE_IT',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'IT支持组排班表：修改'
    },
    {
        'department': 'MODULE_IT',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'IT支持组排班表：删除'
    },
    {
        'department': 'MODULE_UD',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'用户数据中心排班表：查询'

    },
    {
        'department': 'MODULE_UD',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'用户数据中心排班表：创建'

    },
    {
        'department': 'MODULE_UD',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'用户数据中心排班表：修改'

    },
    {
        'department': 'MODULE_UD',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'用户数据中心排班表：删除'

    },
    {
        'department': 'MODULE_VT',
        'management': 'S_MANAGEMENT',
        'codename': 'GET',
        'alias': u'三、四线值班表：查看'
    },
    {
        'department': 'MODULE_VT',
        'management': 'S_MANAGEMENT',
        'codename': 'POST',
        'alias': u'三、四线值班表：创建'
    },
    {
        'department': 'MODULE_VT',
        'management': 'S_MANAGEMENT',
        'codename': 'PUT',
        'alias': u'三、四线值班表：修改'
    },
    {
        'department': 'MODULE_VT',
        'management': 'S_MANAGEMENT',
        'codename': 'DELETE',
        'alias': u'三、四线值班表：删除'
    },
]

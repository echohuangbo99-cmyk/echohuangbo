"""
松鼠AI 异议查询助手 - Flask API 服务
提供 REST API 接口，支持异议查询、智能匹配等功能
可集成到企业系统（钉钉、企业微信、CRM等）
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from objection_assistant import ObjectionAssistant
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化异议助手
assistant = ObjectionAssistant()

# ============ 基础路由 ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': '松鼠AI异议查询助手正在运行',
        'timestamp': datetime.now().isoformat()
    })

# ============ 异议查询 API ============

@app.route('/api/objections', methods=['GET'])
def get_all_objections():
    """获取所有异议"""
    return jsonify({
        'status': 'success',
        'data': assistant.objections,
        'count': len(assistant.objections)
    })

@app.route('/api/objections/<int:objection_id>', methods=['GET'])
def get_objection(objection_id):
    """获取单个异议详情"""
    for obj in assistant.objections:
        if obj['id'] == objection_id:
            assistant.record_usage(objection_id)  # 记录查询
            return jsonify({
                'status': 'success',
                'data': obj
            })
    return jsonify({
        'status': 'error',
        'message': '异议不存在'
    }), 404

@app.route('/api/objections/search', methods=['POST'])
def search_objections():
    """搜索异议"""
    data = request.get_json()
    keyword = data.get('keyword', '')
    
    if not keyword:
        return jsonify({
            'status': 'error',
            'message': '请提供搜索关键词'
        }), 400
    
    results = assistant.search_objections(keyword)
    return jsonify({
        'status': 'success',
        'keyword': keyword,
        'results': results,
        'count': len(results)
    })

@app.route('/api/objections/match', methods=['POST'])
def match_objections():
    """AI 智能匹配"""
    data = request.get_json()
    user_input = data.get('input', '')
    
    if not user_input:
        return jsonify({
            'status': 'error',
            'message': '请提供用户输入'
        }), 400
    
    result = assistant.smart_match(user_input)
    return jsonify({
        'status': 'success',
        'data': result
    })

@app.route('/api/objections/category', methods=['GET'])
def get_by_category():
    """按分类获取异议"""
    category = request.args.get('name', '')
    
    if not category:
        return jsonify({
            'status': 'error',
            'message': '请指定分类'
        }), 400
    
    results = assistant.get_by_category(category)
    return jsonify({
        'status': 'success',
        'category': category,
        'results': results,
        'count': len(results)
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """获取所有分类"""
    categories = assistant.get_all_categories()
    return jsonify({
        'status': 'success',
        'categories': categories,
        'count': len(categories)
    })

# ============ 异议管理 API ============

@app.route('/api/objections', methods=['POST'])
def create_objection():
    """创建新异议"""
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['title', 'category', 'description', 'analysis']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'缺少必填字段: {field}'
            }), 400
    
    obj = assistant.add_objection(data)
    return jsonify({
        'status': 'success',
        'message': '异议已创建',
        'data': obj
    }), 201

@app.route('/api/objections/<int:objection_id>', methods=['PUT'])
def update_objection(objection_id):
    """更新异议"""
    data = request.get_json()
    
    obj = assistant.update_objection(objection_id, data)
    if obj:
        return jsonify({
            'status': 'success',
            'message': '异议已更新',
            'data': obj
        })
    return jsonify({
        'status': 'error',
        'message': '异议不存在'
    }), 404

@app.route('/api/objections/<int:objection_id>', methods=['DELETE'])
def delete_objection(objection_id):
    """删除异议"""
    if assistant.delete_objection(objection_id):
        return jsonify({
            'status': 'success',
            'message': '异议已删除'
        })
    return jsonify({
        'status': 'error',
        'message': '异议不存在'
    }), 404

# ============ 反馈和评分 API ============

@app.route('/api/objections/<int:objection_id>/rate', methods=['POST'])
def rate_objection(objection_id):
    """评分异议"""
    data = request.get_json()
    rating = data.get('rating', 0)
    
    if not (0 <= rating <= 5):
        return jsonify({
            'status': 'error',
            'message': '评分必须在 0-5 之间'
        }), 400
    
    assistant.rate_solution(objection_id, rating)
    return jsonify({
        'status': 'success',
        'message': '评分已保存',
        'objection_id': objection_id,
        'rating': rating
    })

# ============ 统计 API ============

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    stats = assistant.get_statistics()
    return jsonify({
        'status': 'success',
        'data': stats
    })

@app.route('/api/statistics/usage', methods=['GET'])
def get_usage_stats():
    """获取使用统计（最常查询的异议）"""
    sorted_by_usage = sorted(
        assistant.objections,
        key=lambda x: x.get('usageCount', 0),
        reverse=True
    )[:10]
    
    return jsonify({
        'status': 'success',
        'data': sorted_by_usage
    })

# ============ 导出 API ============

@app.route('/api/export/excel', methods=['GET'])
def export_excel():
    """导出为 Excel"""
    try:
        filename = assistant.export_to_excel('/tmp/objections_export.xlsx')
        return jsonify({
            'status': 'success',
            'message': 'Excel 已生成',
            'file': '/tmp/objections_export.xlsx'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """导出为 JSON"""
    try:
        filename = assistant.export_to_json('/tmp/objections_export.json')
        return jsonify({
            'status': 'success',
            'message': 'JSON 已生成',
            'data': assistant.objections
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============ 健康和测试路由 ============

@app.route('/', methods=['GET'])
def index():
    """API 首页"""
    return jsonify({
        'name': '松鼠AI 异议查询助手 API',
        'version': '1.0.0',
        'endpoints': {
            '查询': {
                'GET /api/objections': '获取所有异议',
                'GET /api/objections/<id>': '获取单个异议',
                'POST /api/objections/search': '搜索异议',
                'POST /api/objections/match': 'AI 智能匹配',
                'GET /api/categories': '获取所有分类',
                'GET /api/objections/category?name=<category>': '按分类获取异议',
            },
            '管理': {
                'POST /api/objections': '创建异议',
                'PUT /api/objections/<id>': '更新异议',
                'DELETE /api/objections/<id>': '删除异议',
                'POST /api/objections/<id>/rate': '评分异议',
            },
            '统计': {
                'GET /api/statistics': '获取统计数据',
                'GET /api/statistics/usage': '获取使用统计',
                'GET /api/export/excel': '导出 Excel',
                'GET /api/export/json': '导出 JSON',
            }
        }
    })

# ============ 错误处理 ============

@app.errorhandler(404)
def not_found(error):
    """404 处理"""
    return jsonify({
        'status': 'error',
        'message': '资源不存在',
        'code': 404
    }), 404

@app.errorhandler(500)
def server_error(error):
    """500 处理"""
    return jsonify({
        'status': 'error',
        'message': '服务器错误',
        'code': 500
    }), 500

# ============ 测试数据加载 ============

def load_sample_data():
    """加载示例数据（如果数据库为空）"""
    if not assistant.objections:
        sample_data = [
            {
                'title': '价格太贵，竞品更便宜',
                'category': '价格相关',
                'keywords': ['价格', '贵', '便宜', '成本'],
                'description': '客户认为产品价格过高',
                'analysis': '反映客户对产品价值认知不足',
                'solutions': ['强调长期ROI', '对标竞品', '分期支付方案'],
                'dataPoints': ['续费率92%', '投资回报周期3-6个月'],
                'counterExamples': ['张女士用3个月续费3年', '李先生半年后跳槽过来'],
                'tips': ['不要直接降价', '强调长期价值', '讲真实案例']
            },
            {
                'title': '效果不明显，不如线下培训',
                'category': '产品效果',
                'keywords': ['效果', '没效果', '线下'],
                'description': '客户怀疑线上AI教学效果',
                'analysis': '客户对AI教学效果认知gap',
                'solutions': ['数据对标', '个性化优势', '免费试用'],
                'dataPoints': ['平均提分15-30分', '学习专注度提升40%'],
                'counterExamples': ['王同学3个月从75分到92分'],
                'tips': ['讲具体数据', '强调个性化', '邀请试用']
            }
        ]
        
        for data in sample_data:
            assistant.add_objection(data)

if __name__ == '__main__':
    # 加载示例数据
    load_sample_data()
    
    # 启动服务
    print("=" * 60)
    print("🚀 松鼠AI 异议查询助手 API 启动")
    print("=" * 60)
    print("📡 访问地址: http://localhost:5000")
    print("📚 API 文档: http://localhost:5000/")
    print("=" * 60)
    
    # 开发环境
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # 生产环境建议使用 gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app

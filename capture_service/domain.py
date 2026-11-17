"""解释公开通知及引用链。"""
import json
def decode(raw,receipt):
    d=json.loads(raw.decode('utf-8'))
    if d.get('kind') not in ('stop','correction','release'):raise ValueError('通知种类非法')
    return [{'type':'notice','id':d['doc_no'],'version':d['revision'],
             'payload':{'kind':d['kind'],'approval':d['approval'],'batch':d['batch'],
                        'references':d['references'],'effective':d['effective']}}]
def assess(rows):
    notices={r['id']:r for r in rows if r['type']=='notice'}
    reasons=['引用公告未接收:'+ref for r in rows for ref in r['payload']['references'] if ref not in notices]
    if not any(r['payload']['kind']=='release' for r in rows):reasons.append('尚无正式解除依据')
    return {'publishable':not reasons,'reasons':reasons,'notice_ids':sorted(notices)}

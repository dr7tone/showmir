from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from app.Security.auth import get_current_admin_role
from app.database.database import SessionDep
from app.database.models import User_Model
from app.routes.admins import change_user_balance
router = APIRouter(
    prefix="/nfc_tags",
    tags=["NFC Tags"] 
)



@router.get("/{user_id}")
async def get_nfc_tag(user_id: int, session: SessionDep, request: Request): #там костыль лютый если будем делать что то глобальное - надо переделать
    current_role = get_current_admin_role(request)
    if current_role == "admin":
        return await change_user_balance(user_id, session, request)
    else:
        query = select(User_Model).where(User_Model.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return HTMLResponse(f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                    <title>Баланс пользователя #{user_id}</title>
                    <style>
                        * {{ 
                            margin: 0; 
                            padding: 0; 
                            box-sizing: border-box; 
                        }}
                        
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                                        'Helvetica Neue', Arial, sans-serif;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            min-height: 100vh;
                            min-height: 100dvh;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            padding: 16px;
                        }}
                        
                        .card {{
                            background: white;
                            padding: 32px 24px;
                            border-radius: 24px;
                            text-align: center;
                            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                            width: 100%;
                            max-width: 400px;
                            transition: all 0.3s ease;
                        }}
                        
                        .user-id {{
                            color: #718096;
                            font-size: 13px;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            font-weight: 600;
                        }}
                        
                        .user-id-number {{
                            font-size: 28px;
                            font-weight: 700;
                            color: #2d3748;
                            margin: 8px 0 16px 0;
                        }}
                        
                        .balance-wrapper {{
                            background: #f7fafc;
                            border-radius: 16px;
                            padding: 24px 20px;
                            margin: 8px 0 16px 0;
                        }}
                        
                        .balance {{
                            font-size: 48px;
                            font-weight: 800;
                            color: #48bb78;
                            line-height: 1;
                        }}
                        
                        .currency {{
                            font-size: 20px;
                            color: #a0aec0;
                            font-weight: 600;
                            margin-left: 2px;
                        }}
                        
                        .sub-info {{
                            color: #a0aec0;
                            font-size: 12px;
                            margin-top: 8px;
                        }}
                        
                        .back {{
                            display: inline-block;
                            margin-top: 12px;
                            color: #667eea;
                            text-decoration: none;
                            font-weight: 600;
                            font-size: 15px;
                            padding: 10px 24px;
                            border-radius: 12px;
                            background: #edf2f7;
                            transition: all 0.2s ease;
                        }}
                        
                        .back:hover {{
                            background: #e2e8f0;
                        }}
                        
                        .back:active {{
                            transform: scale(0.95);
                        }}
                        
                        /* Адаптация для маленьких экранов */
                        @media (max-width: 480px) {{
                            .card {{
                                padding: 24px 16px;
                                border-radius: 20px;
                            }}
                            
                            .user-id {{
                                font-size: 11px;
                            }}
                            
                            .user-id-number {{
                                font-size: 24px;
                            }}
                            
                            .balance-wrapper {{
                                padding: 16px 12px;
                            }}
                            
                            .balance {{
                                font-size: 36px;
                            }}
                            
                            .currency {{
                                font-size: 18px;
                            }}
                        }}
                        
                        /* Адаптация для очень маленьких экранов */
                        @media (max-width: 360px) {{
                            .card {{
                                padding: 16px 12px;
                            }}
                            
                            .balance {{
                                font-size: 28px;
                            }}
                            
                            .balance-wrapper {{
                                padding: 12px 8px;
                            }}
                        }}
                        
                        /* Адаптация для больших экранов */
                        @media (min-width: 768px) {{
                            .card {{
                                padding: 48px 40px;
                            }}
                            
                            .balance {{
                                font-size: 64px;
                            }}
                        }}
                        
                        /* Поддержка темной темы (опционально) */
                        @media (prefers-color-scheme: dark) {{
                            .card {{
                                background: #1a202c;
                            }}
                            
                            .user-id-number {{
                                color: #e2e8f0;
                            }}
                            
                            .balance-wrapper {{
                                background: #2d3748;
                            }}
                            
                            .back {{
                                background: #2d3748;
                                color: #90cdf4;
                            }}
                            
                            .back:hover {{
                                background: #4a5568;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="card">
                        <div class="user-id">👤 ID пользователя</div>
                        <div class="user-id-number">#{user_id}</div>
                        <div class="balance-wrapper">
                            <div>
                                <span class="balance">{user.balance}</span>
                                <span class="currency">очка</span>
                            </div>
                            <div class="sub-info">Баланс на {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}</div>
                        </div>
                    </div>
                </body>
                </html>
                """)
        else:
            return {"error": "User not found"}
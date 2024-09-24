<a href="{% url 'my_profile:dashboard1' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-tachometer mr-3'></i> Dashboard
                </a>
                <a href="{% url 'user_account:account_balance' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-user mr-3'></i> Profile
                </a>
                <a href="{% url 'withdrawals:request_withdrawal' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-credit-card mr-3'></i> Payment Agents
                </a>
                <a href="{% url 'referrals:referrals' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-user-plus mr-3'></i> Referral
                </a>
                <a href="{% url 'my_profile:complaints' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-error-circle mr-3'></i> Complaints
                </a>
                <a href="{% url 'my_profile:guide' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-book mr-3'></i> Guide
                </a>
                <a href="{% url 'whatsapp_status' %}" class="block px-4 py-2 mt-2 hover:bg-blue-700 rounded transition duration-200">
                    <i class='bx bx-video mr-3'></i> Global views
                </a>
                <a href="{% url 'my_profile:user' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-cog mr-3'></i> Settings
                </a>
                <a href="{% url 'auth_app:login' %}" class="flex items-center px-4 py-3 mb-3 hover-gradient rounded-lg transition-all">
                    <i class='bx bx-log-out mr-3'></i> Logout
                </a>
{% if messages %}
    {% for message in messages %}
    <div 
        id="toast-{{ forloop.counter }}"
        class="fixed top-5 right-5 z-50 flex items-center gap-3 bg-white border border-gray-200 shadow-lg rounded-lg px-4 py-3 text-sm text-gray-800"
    >
        <svg class="w-5 h-5 text-green-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd"/>
        </svg>
        {{ message }}
    </div>
    {% endfor %}

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('[id^="toast-"]').forEach(toast => {
                setTimeout(() => {
                    toast.style.transition = 'opacity 0.5s ease';
                    toast.style.opacity = '0';
                    setTimeout(() => toast.remove(), 500);
                }, 3000);
            });
        });
    </script>
{% endif %}
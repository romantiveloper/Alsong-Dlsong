const toggleBtn = document.querySelector('.navbar__toggleBtn');
const menu = document.querySelector('.navbar__menu');
const signBtn = document.getElementById('signBtn');
const kakaoBtn = document.getElementById('kakao-btn')
const findBtn = document.getElementById('find')
const hiddenBox = document.getElementById('hidden_box')
const findPw = document.getElementById('find_pw')

toggleBtn.addEventListener('click', () => {
  menu.classList.toggle('active');
  icons.classList.toggle('active');
});

$('.search-input').focus(function(){
    $(this).parent().addClass('focus');
  }).blur(function(){
    $(this).parent().removeClass('focus');
  })

// 회원가입 스크립트를 화살표 함수에서 기존 함수로 변경
signBtn.addEventListener('click', function () {
  const username = $('#username').val();
  const user_id = $('#user_id').val();
  const password1 = $('#password1').val();
  const password2 = $('#password2').val();
  const nickname = $('#nickname').val();
  const email = $('#email').val();
  const birthday = $('#birthday').val();
  const gender = $('#gender').val();

  $.ajax({
      type: 'POST',
      url: '/user/sign-up/',
      data: JSON.stringify({
          username: username,
          user_id: user_id,
          password1: password1,
          password2: password2,
          nickname: nickname,
          email: email,
          birthday: birthday,
          gender: gender,
      }),
      success: function (data) {
          alert(data.message);
          location.replace('{% url "user:sign-in" %}');
      },
      error: function (request, status, error) {
          const data = JSON.parse(request.responseText);
          console.log(data.message);
          alert(data.message);
      },
      beforeSend: function (xhr) {
          xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
      },
  });
});


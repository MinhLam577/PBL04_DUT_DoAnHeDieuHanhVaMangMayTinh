        // Lấy tất cả các thẻ li
        var liElements = document.querySelectorAll('aside ul li');

        // Lặp qua từng thẻ li
        liElements.forEach(function (liElement) {
            // Thêm sự kiện click
            liElement.addEventListener('click', function (event) {
                // Kiểm tra xem thẻ đang click có đang mở hay không
                var isOpen = liElement.style.maxHeight === '300px';

                // Đóng tất cả các thẻ đang mở
                liElements.forEach(function (element) {
                    element.style.maxHeight = '35px'; // Đặt lại chiều cao của các thẻ về giá trị mặc định
                });

                // Nếu thẻ đang click không đang mở, mở nó. Nếu đang mở, đóng nó.
                if (!isOpen) {
                    liElement.style.maxHeight = '300px';
                }
            });
        });
        function SelectItemMenu(giatri, duongdan) {
            if(giatri == 1) {
                document.getElementById('frame').src = duongdan;
            }
            else if(giatri == 2) {
                document.getElementById('frame').src = duongdan;
            }else if(giatri == 3) {
                document.getElementById('frame').src = duongdan;
            }

        }
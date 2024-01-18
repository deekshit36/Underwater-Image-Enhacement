$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
                // $('#imagePreviewResult').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreviewResult').hide();
                $('#imagePreviewResult').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
       
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        $('.image-section-result').hide()
        $('#imagePreviewResult').hide();
        // $('#imagePreviewResult').css('background-image', 'url()');
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // const resultImage = document.getElementById('resultImage');
        // $('.image-section-result').show();
        // Show loading animation
        $(this).hide();
        $('.loader').show();
        var timestamp =  new Date().getTime();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#imagePreviewResult').css('background-image', 'url(' + data + '?'+ timestamp +')');
                // $('#imagePreviewResult').html('<img src="${data}" alt="Result Image">');
                $('.image-section-result').show()
                $('#imagePreviewResult').show();
                
                // resultImage.src=data;
                // document.getElementById("imagePreviewResult").src =data
                // $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                $('#result').show();
                console.log('Success!');
            },
        });
    });

});

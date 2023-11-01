import numpy as np
from pytest import raises, fixture

from delivery_api.models.delivery_prediction import DeliveryPrediction
from delivery_api.models.preprocessed_order import PreprocessedOrder
from delivery_api.services.model_service import ModelService


@fixture
def mock_xgb_regressor(mocker):
    mock = mocker.patch(
        'delivery_api.services.model_service.XGBRegressor',
        autospec=True
    )
    return mock


def test_load_model_success(mock_xgb_regressor, monkeypatch):
    # Arrange
    monkeypatch.setenv('MODEL_WEIGHTS_PATH', 'fake_model_path.json')

    # Act
    ModelService()

    # Assert
    mock_xgb_regressor.assert_called_once()
    mock_xgb_regressor.return_value \
        .load_model.assert_called_once_with('fake_model_path.json')


def test_load_model_without_env(monkeypatch):
    # Arrange
    monkeypatch.delenv('MODEL_WEIGHTS_PATH', raising=False)

    # Act and assert
    with raises(AssertionError):
        ModelService()


@fixture
def preprocessed_order():
    order = PreprocessedOrder(
        is_retail=1,
        avg_preparation_time=30.0,
        hour_of_day=14
    )
    return order


@fixture
def model_service(mocker):
    mocker.patch.object(ModelService, '_load_model')
    service = ModelService()  # _load_model will not be executed
    # Mock the model's predict method
    service.model = mocker.MagicMock()
    service.model.predict.return_value = np.array([1200])
    return service


def test_predict_successful(model_service, preprocessed_order):
    # Arrange
    expected_data_for_prediction = np.array([
        preprocessed_order.is_retail,
        preprocessed_order.avg_preparation_time,
        preprocessed_order.hour_of_day
    ]).reshape(1, -1)

    # Act
    prediction = model_service.predict(preprocessed_order)

    # Assert
    # Assert that predict method of the model was called correctly
    model_service.model.predict.assert_called_once()

    # Verify the input to the predict method was as expected
    actual_call_args = model_service.model.predict.call_args[0][0]
    np.testing.assert_array_equal(actual_call_args, expected_data_for_prediction)

    # Assert the result is an instance of DeliveryPrediction with the correct delivery_duration
    assert isinstance(prediction, DeliveryPrediction)
    assert prediction.delivery_duration == 1200

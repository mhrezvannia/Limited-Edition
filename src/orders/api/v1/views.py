from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from orders.models import Cart, CartProduct
from website.models import Product
from .serializers import CartSerializer, CartProductSerializer


class CartCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        cart, created = Cart.objects.get_or_create(customer_id=user_id)

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

# global execption traif mikoni
class AddItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            # Ensure quantity is a valid integer and greater than 0
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                return Response(
                    {"error": "Quantity must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # Ensure the product exists
                product = Product.objects.get(id=product_id)

                # Get or create the cart for the user
                cart, created = Cart.objects.get_or_create(customer_id=request.user.id)

                # Add the product to the cart or update its quantity
                cart_product, created = CartProduct.objects.get_or_create(
                    cart=cart,
                    product=product,  # Use the product object
                    defaults={'quantity': quantity}
                )
                if not created:
                    # Update quantity if product already exists in the cart
                    cart_product.quantity += quantity
                    cart_product.save()

                return Response(CartProductSerializer(cart_product).data, status=status.HTTP_200_OK)

            except Product.DoesNotExist:
                return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
            except Cart.DoesNotExist:
                return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     product_id = request.data.get('product_id')
    #     quantity = request.data.get('quantity')
    #
    #     # Ensure product_id and quantity are present
    #     if not product_id or not quantity:
    #         return Response(
    #             {"error": "Both 'product_id' and 'quantity' are required."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #
    #     # Ensure quantity is a valid integer and greater than 0
    #     try:
    #         quantity = int(quantity)
    #         if quantity <= 0:
    #             raise ValueError
    #     except ValueError:
    #         return Response(
    #             {"error": "Quantity must be a positive integer."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #
    #     try:
    #         # Ensure the product exists
    #         product = Product.objects.get(id=product_id)
    #
    #         # Get or create the cart for the user
    #         cart, created = Cart.objects.get_or_create(customer_id=request.user.id)
    #
    #         # Add the product to the cart or update its quantity
    #         cart_product, created = CartProduct.objects.get_or_create(
    #             cart=cart,
    #             product=product,  # Use the product object
    #             defaults={'quantity': quantity}
    #         )
    #         if not created:
    #             # Update quantity if product already exists in the cart
    #             cart_product.quantity += quantity
    #             cart_product.save()
    #
    #         return Response(CartProductSerializer(cart_product).data, status=status.HTTP_200_OK)
    #
    #     except Product.DoesNotExist:
    #         return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
    #     except Cart.DoesNotExist:
    #         return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get('product_id')

        try:
            cart = Cart.objects.get(customer_id=request.user.id)
            cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)
            cart_product.delete()

            return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)

        except CartProduct.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            cart = Cart.objects.get(customer_id=request.user.id)
            cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)
            cart_product.quantity = quantity
            cart_product.save()

            return Response(CartProductSerializer(cart_product).data, status=status.HTTP_200_OK)

        except CartProduct.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(customer_id=request.user.id)
            cart_products = CartProduct.objects.filter(cart=cart)

            return Response(CartProductSerializer(cart_products, many=True).data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
